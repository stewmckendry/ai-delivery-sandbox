import os
import json
import asyncio
import importlib
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime
import logging
import fitz  # PyMuPDF
from dotenv import load_dotenv

load_dotenv()

import httpx

from app import crawler, extractor, cleaner

from app.storage.files import save_file, delete_file
from app.storage.db import init_db, SessionLocal
from app.processors.lab_pdf_parser import extract_lab_results_with_date
from app.processors.visit_html_parser import extract_visit_summaries
from app.processors.structuring import insert_lab_results, insert_visit_summaries
from app.utils import chat_completion
from app.storage.structured import insert_structured_records
from app.storage.credentials import get_credentials, delete_credentials
from app.adapters.common import challenges
from app.storage.audit import log_event
from app.prompts.summarizer import summarize_database_records
import re
from app.storage import blob

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)

# Delete files in data/raw after processing if set
DELETE_RAW = os.getenv("RAW_CLEANUP", "0").lower() in {"1", "true", "yes"}


# heuristic keyword mapping for clinical types (fallback)
CLINICAL_MAPPINGS = [
    (
        re.compile(r"\bmetformin\b", re.I),
        ("MedicationStatement", "860975", "RxNorm", "Metformin"),
    ),
    (
        re.compile(r"\bdiabetes\b", re.I),
        ("Condition", "44054006", "SNOMED", "Diabetes mellitus"),
    ),
    (re.compile(r"\basthma\b", re.I), ("Condition", "195967001", "SNOMED", "Asthma")),
    (re.compile(r"allerg", re.I), ("AllergyIntolerance", None, None, None)),
    (re.compile(r"immunization|vaccine", re.I), ("Immunization", None, None, None)),
    (
        re.compile(r"surg|procedure|operation|imaging|scan", re.I),
        ("Procedure", None, None, None),
    ),
    (
        re.compile(r"blood pressure|\bbp\b", re.I),
        ("VitalSigns", "85354-9", "LOINC", "Blood pressure"),
    ),
    (re.compile(r"height", re.I), ("VitalSigns", "8302-2", "LOINC", "Body height")),
    (re.compile(r"weight", re.I), ("VitalSigns", "29463-7", "LOINC", "Body weight")),
    (
        re.compile(r"diagnostic report|radiology|x-ray|ct|mri", re.I),
        ("DiagnosticReport", None, None, None),
    ),
]


def _classify_clinical_type(
    text: str,
) -> tuple[str | None, str | None, str | None, str | None]:
    """Return clinical type and optional code mappings for ``text`` using an LLM with regex fallback."""

    prompt = (
        "What FHIR resource type best fits this clinical text? "
        "Respond ONLY with a JSON object containing the keys "
        "'clinical_type', 'code', 'code_system', 'display'.\nText: " + text
    )
    try:
        resp = chat_completion([{"role": "user", "content": prompt}])
        cleaned = resp.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?", "", cleaned)
            cleaned = cleaned.rstrip("`").strip()
        if cleaned.lower().startswith("json:"):
            cleaned = cleaned[5:].strip()
        info = json.loads(cleaned)
        if isinstance(info, dict) and info.get("clinical_type"):
            return (
                info.get("clinical_type"),
                info.get("code"),
                info.get("code_system"),
                info.get("display"),
            )
    except Exception as exc:  # noqa: BLE001
        logger.warning("[etl] LLM clinical classification failed: %s", exc)

    for pattern, result in CLINICAL_MAPPINGS:
        if pattern.search(text):
            return result
    return None, None, None, None


def _load_scraper(portal_name: str):
    module = importlib.import_module(f"app.adapters.{portal_name}")
    func_name = f"scrape_{portal_name}"
    scraper = getattr(module, func_name, None)
    if scraper is None:
        raise AttributeError(f"Scraper function '{func_name}' not found")
    return scraper


def _run_scraper(
    scraper,
    portal_name: str,
    username: str | None = None,
    password: str | None = None,
):
    """Execute scraper with credentials or environment fallbacks."""
    env_user = os.getenv(f"{portal_name.upper()}_USERNAME")
    env_pass = os.getenv(f"{portal_name.upper()}_PASSWORD")
    url = os.getenv(f"{portal_name.upper()}_URL")

    username = username or env_user
    password = password or env_pass

    args = []
    if username:
        args.append(username)
    if password:
        args.append(password)
    if url:
        args.append(url)

    if asyncio.iscoroutinefunction(scraper):
        result = asyncio.run(scraper(*args))
    else:
        result = scraper(*args)

    # Support paused login sessions returned by scrapers
    while isinstance(result, dict) and result.get("challenge_id"):
        cid = result["challenge_id"]
        logger.info("[etl] Waiting for challenge %s", cid)
        code = asyncio.run(challenges._await_response(cid))
        logger.info("[etl] Resuming challenge %s", cid)
        resume = result.get("resume")
        if resume:
            if asyncio.iscoroutinefunction(resume):
                result = asyncio.run(resume(code))
            else:
                result = resume(code)
        else:
            break

    return result


def _extract_file_paths(result):
    if isinstance(result, dict) and "files" in result:
        files = result["files"]
    else:
        files = result
    paths = []
    for item in files:
        if isinstance(item, dict) and "file_path" in item:
            paths.append(item["file_path"])
        else:
            paths.append(str(item))
    return paths


def run_etl_for_portal(portal_name: str, user_id: str | None = None) -> str:
    """Run scraping, parsing and DB insertion for ``portal_name``.

    Returns a markdown summary of all extracted records.
    """
    user = user_id or os.getenv("ETL_USER", "system")
    log_event(
        user,
        "consent_granted",
        {"portal": portal_name, "timestamp": datetime.utcnow().isoformat()},
    )
    logger.info("[etl] Starting pipeline for %s", portal_name)
    scraper = _load_scraper(portal_name)

    logger.info("[creds] Retrieving credentials for %s", portal_name)
    creds = get_credentials(portal_name)
    if creds:
        logger.info("[creds] Credentials found for %s", portal_name)
    else:
        logger.info("[creds] Credentials missing or expired for %s", portal_name)

    log_event(user, "login", {"portal": portal_name})

    logger.info("[etl] Running scraper %s", scraper.__name__)
    result = _run_scraper(
        scraper,
        portal_name,
        creds.get("username") if creds else None,
        creds.get("password") if creds else None,
    )
    delete_credentials(portal_name)
    logger.info("[creds] Deleted credentials for %s", portal_name)

    file_paths = _extract_file_paths(result)
    logger.info("[etl] %d files scraped", len(file_paths))
    log_event(user, "scrape", {"portal": portal_name, "file_count": len(file_paths)})

    init_db()
    session = SessionLocal()
    labs_all = []
    visits_all = []
    try:
        for path_str in file_paths:
            path = Path(path_str)
            if not path.exists():
                continue
            content = path.read_bytes()
            saved = save_file(content, path.name, portal_name, {"source": path_str})
            if path.suffix.lower() == ".pdf":
                logger.info("[etl] Parsing labs from %s", path_str)
                labs = extract_lab_results_with_date(path_str)
                labs_all.extend(labs)
            else:
                logger.info("[etl] Parsing visits from %s", path_str)
                html = content.decode("utf-8", errors="ignore")
                visits = extract_visit_summaries(html)
                visits_all.extend(visits)
            if DELETE_RAW:
                delete_file(saved)
        log_event(
            user,
            "parse",
            {
                "portal": portal_name,
                "files": len(file_paths),
                "labs": len(labs_all),
                "visits": len(visits_all),
            },
        )
        if labs_all:
            logger.info("[etl] Inserting %d lab results", len(labs_all))
            insert_lab_results(session, labs_all, session_key=user)
        if visits_all:
            logger.info("[etl] Inserting %d visit summaries", len(visits_all))
            insert_visit_summaries(session, visits_all, session_key=user)
        if labs_all or visits_all:
            log_event(
                user,
                "insert",
                {
                    "portal": portal_name,
                    "labs": len(labs_all),
                    "visits": len(visits_all),
                },
            )

        # ------------------------------------------------------------------
        # AI-powered extraction pipeline
        # ------------------------------------------------------------------
        html_pages = []
        for path_str in file_paths:
            path = Path(path_str)
            if path.suffix.lower() != ".pdf" and path.exists():
                html_pages.append(
                    {
                        "url": path_str,
                        "html": path.read_text(encoding="utf-8", errors="ignore"),
                        "capture_method": "html",
                        "source": "operator",
                    }
                )

        if html_pages:
            try:
                limit = int(os.getenv("MAX_DEPTH", "3"))
            except ValueError:
                limit = 3

            base_url = os.getenv(f"{portal_name.upper()}_URL", html_pages[0]["url"])

            def fetch_html(url: str) -> str:
                parsed = urlparse(url)
                if parsed.scheme in {"", "file"}:
                    p = Path(parsed.path)
                    if p.exists():
                        return p.read_text(encoding="utf-8", errors="ignore")
                    return ""
                try:
                    resp = httpx.get(url, timeout=10)
                    resp.raise_for_status()
                    return resp.text
                except Exception:
                    return ""

            crawled, _ = crawler.crawl_portal(
                html_pages[0]["html"], base_url, fetch_html, limit=limit
            )
            for page in crawled:
                if page["url"] not in {p["url"] for p in html_pages}:
                    html_pages.append(page)

            extracted = []
            for page in html_pages:
                records = extractor.extract_relevant_content(page["html"], page["url"])
                for rec in records:
                    rec["portal"] = portal_name
                    rec["capture_method"] = page.get("capture_method", "html")
                    rec["source"] = page.get("source", "operator")
                extracted.extend(records)

            cleaned = cleaner.clean_blocks(extracted)

            mapping = {}
            for rec in extracted:
                mapping.setdefault(rec.get("text", ""), rec)

            final_records = []
            for text in cleaned:
                meta = mapping.get(text, {})
                ctype, code, system, display = _classify_clinical_type(text)
                final_records.append(
                    {
                        "portal": portal_name,
                        "source_url": meta.get("source_url", ""),
                        "type": meta.get("type", ""),
                        "clinical_type": ctype,
                        "code": code,
                        "code_system": system,
                        "display": display,
                        "text": text,
                        "source": meta.get("source", "operator"),
                        "capture_method": meta.get("capture_method", "html"),
                        "user_notes": meta.get("user_notes", ""),
                    }
                )

            if final_records:
                logger.info(
                    "[etl] Inserting %d structured records for session %s",
                    len(final_records),
                    user,
                )
                insert_structured_records(session, final_records, session_key=user)

            summary = ""
            try:
                summary = summarize_database_records(session)
                logger.info(summary)
            except Exception as exc:  # noqa: BLE001
                logger.error("[etl] Failed to generate summary: %s", exc)

            logger.info(json.dumps(final_records, indent=2))
    finally:
        session.close()
        logger.info("[etl] ETL complete for session %s", user)
    return summary


def _pdf_to_text(path: str | Path) -> str:
    """Return plain text from a PDF file."""
    text = ""
    with fitz.open(path) as doc:  # type: ignore[attr-defined]
        for page in doc:
            text += page.get_text("text")
    if not text.strip():
        logger.info("[etl] No embedded text found, OCR pipeline pending")
    return text


def _annotate_labs_with_llm(labs: list[dict]) -> list[dict]:
    """Use an LLM to assign LOINC codes and FHIR Observations."""
    if not labs:
        return labs
    prompt = (
        "For each lab result entry in the following JSON, provide a 'loinc_code'"
        " and a minimal FHIR Observation object. Return a JSON array in the same"
        " order as the input.\nEntries:\n" + json.dumps(labs)
    )
    try:
        content = chat_completion([{"role": "user", "content": prompt}])
        info = json.loads(content)
    except Exception as exc:  # noqa: BLE001
        logger.error("[etl] LLM lab annotation failed: %s", exc)
        return labs
    if isinstance(info, dict):
        info = [info]
    for entry, upd in zip(labs, info):
        if isinstance(upd, dict):
            if upd.get("loinc_code"):
                entry["loinc_code"] = upd["loinc_code"]
            if upd.get("fhir"):
                entry["fhir"] = upd["fhir"]
    return labs


def _annotate_visits_with_llm(visits: list[dict]) -> list[dict]:
    """Use an LLM to assign SNOMED codes and FHIR Encounters."""
    if not visits:
        return visits
    prompt = (
        "For each visit entry in the following JSON, provide a 'snomed_code' and"
        " a minimal FHIR Encounter object. Return a JSON array in the same order"
        " as the input.\nEntries:\n" + json.dumps(visits)
    )
    try:
        content = chat_completion([{"role": "user", "content": prompt}])
        info = json.loads(content)
    except Exception as exc:  # noqa: BLE001
        logger.error("[etl] LLM visit annotation failed: %s", exc)
        return visits
    if isinstance(info, dict):
        info = [info]
    for entry, upd in zip(visits, info):
        if isinstance(upd, dict):
            if upd.get("snomed_code"):
                entry["snomed_code"] = upd["snomed_code"]
            if upd.get("fhir"):
                entry["fhir"] = upd["fhir"]
    return visits


def _detect_labs_and_visits_with_llm(
    records: list[dict],
) -> tuple[list[dict], list[dict]]:
    """Classify ``records`` text as labs or visits and extract structured data."""
    if not records:
        return [], []
    texts = [r.get("text", "") for r in records]
    prompt = (
        "For each entry in the following JSON array, classify it as a lab or visit and "
        "return structured data. Use the format:\n"
        "{type: 'lab', test_name: '', value: '', units: '', date: ''} or\n"
        "{type: 'visit', provider: '', doctor: '', notes: '', date: ''} or {type: 'other'}.\n"
        "Entries:\n" + json.dumps(texts)
    )
    try:
        content = chat_completion([{"role": "user", "content": prompt}])
        info = json.loads(content)
    except Exception as exc:  # noqa: BLE001
        logger.error("[etl] LLM record classification failed: %s", exc)
        return [], []
    if isinstance(info, dict):
        info = [info]
    labs: list[dict] = []
    visits: list[dict] = []
    for item in info:
        if not isinstance(item, dict):
            continue
        if item.get("type") == "lab":
            labs.append(item)
        elif item.get("type") == "visit":
            visits.append(item)
    return labs, visits


def run_etl_from_blobs(prefix: str, user_id: str | None = None) -> str:
    """Process files uploaded to Azure Blob under ``prefix`` and return summary."""

    user = user_id or os.getenv("ETL_USER", "system")
    logger.info("[etl] Starting blob pipeline for %s", prefix)
    log_event(user, "blob_fetch", {"prefix": prefix})

    blob_names = blob.list_blobs(prefix)
    logger.info("[etl] %d blobs found", len(blob_names))
    if not blob_names:
        logger.error("[etl] No blobs found for session %s", prefix)

    init_db()
    session = SessionLocal()

    pages: list[dict[str, str]] = []

    try:
        for name in blob_names:
            if not name.startswith(prefix):
                continue
            filename = os.path.basename(name)
            if ".." in filename or filename.startswith(("/", "\\")):
                continue
            data = blob.download_blob(name)
            path = save_file(data, filename, "blob", {"source": name})
            suffix = Path(filename).suffix.lower()
            if suffix == ".pdf":
                logger.info("[etl] Extracting text from %s", name)
                text = _pdf_to_text(path)
            else:
                text = data.decode("utf-8", errors="ignore")
            method = (
                "pdf"
                if suffix == ".pdf"
                else ("html" if suffix in {".html", ".htm"} else "screenshot")
            )
            pages.append(
                {
                    "url": name,
                    "text": text,
                    "filename": filename,
                    "capture_method": method,
                    "source": "operator",
                }
            )
            blob.delete_blob(name)
            if DELETE_RAW:
                delete_file(path)

        logger.info("[etl] Loaded %d pages", len(pages))
        extracted = []
        for page in pages:
            records = extractor.extract_relevant_content(page["text"], page["url"])
            for rec in records:
                rec["portal"] = "blob"
            extracted.extend(records)
        logger.info("[etl] Extracted %d records", len(extracted))

        final_records = []
        if extracted:
            cleaned = cleaner.clean_blocks(extracted)
            mapping = {}
            for rec in extracted:
                mapping.setdefault(rec.get("text", ""), rec)

            for text in cleaned:
                meta = mapping.get(text, {})
                ctype, code, system, display = _classify_clinical_type(text)
                final_records.append(
                    {
                        "portal": "blob",
                        "source_url": meta.get("source_url", ""),
                        "type": meta.get("type", ""),
                        "clinical_type": ctype,
                        "code": code,
                        "code_system": system,
                        "display": display,
                        "text": text,
                        "source": meta.get("source", "operator"),
                        "capture_method": meta.get("capture_method", ""),
                        "user_notes": meta.get("user_notes", ""),
                    }
                )
        if final_records:
            logger.info("[etl] Classified %d records", len(final_records))

        if final_records:
            logger.info(
                "[etl] Inserting %d structured records for session %s",
                len(final_records),
                prefix,
            )
            saved_records = insert_structured_records(session, final_records, session_key=prefix)
            try:
                from app.rag.indexer import index_structured_records
                logger.info(
                    "[rag.indexer] Indexing %d structured records to Chroma for session %s",
                    len(saved_records),
                    prefix,
                )
                index_structured_records(saved_records, prefix)
                logger.info(
                    "[rag.indexer] Chroma indexing complete for session %s", prefix
                )
            except Exception as exc:  # noqa: BLE001
                logger.error("[etl] Vector index failed: %s", exc)

        # detect labs and visits from structured records
        labs, visits = _detect_labs_and_visits_with_llm(final_records)
        if labs:
            labs = _annotate_labs_with_llm(labs)
            insert_lab_results(session, labs, session_key=prefix)

        if visits:
            visits = _annotate_visits_with_llm(visits)
            insert_visit_summaries(session, visits, session_key=prefix)

        summary = ""
        if final_records:
            try:
                summary = summarize_database_records(session)
                logger.info(summary)
            except Exception as exc:  # noqa: BLE001
                logger.error("[etl] Failed to generate summary: %s", exc)
    finally:
        session.close()
        logger.info("[etl] ETL complete for session %s", prefix)
    return summary
