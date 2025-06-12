import os
import asyncio
import importlib
from pathlib import Path

from app.storage.files import save_file
from app.storage.db import init_db, SessionLocal
from app.processors.lab_pdf_parser import extract_lab_results_with_date
from app.processors.visit_html_parser import extract_visit_summaries
from app.processors.structuring import insert_lab_results, insert_visit_summaries
from app.storage.credentials import get_credentials, delete_credentials


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
        return asyncio.run(scraper(*args))
    return scraper(*args)


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


def run_etl_for_portal(portal_name: str) -> None:
    """Run scraping, parsing and DB insertion for ``portal_name``."""
    print(f"[etl] Starting pipeline for {portal_name}")
    scraper = _load_scraper(portal_name)

    print(f"[creds] Retrieving credentials for {portal_name}")
    creds = get_credentials(portal_name)
    if creds:
        print(f"[creds] Credentials found for {portal_name}")
    else:
        print(f"[creds] Credentials missing or expired for {portal_name}")

    print(f"[etl] Running scraper {scraper.__name__}")
    result = _run_scraper(
        scraper,
        portal_name,
        creds.get("username") if creds else None,
        creds.get("password") if creds else None,
    )
    delete_credentials(portal_name)
    print(f"[creds] Deleted credentials for {portal_name}")

    file_paths = _extract_file_paths(result)
    print(f"[etl] {len(file_paths)} files scraped")

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
            save_file(content, path.name, portal_name, {"source": path_str})
            if path.suffix.lower() == ".pdf":
                print(f"[etl] Parsing labs from {path_str}")
                labs = extract_lab_results_with_date(path_str)
                labs_all.extend(labs)
            else:
                print(f"[etl] Parsing visits from {path_str}")
                html = content.decode("utf-8", errors="ignore")
                visits = extract_visit_summaries(html)
                visits_all.extend(visits)
        if labs_all:
            print(f"[etl] Inserting {len(labs_all)} lab results")
            insert_lab_results(session, labs_all)
        if visits_all:
            print(f"[etl] Inserting {len(visits_all)} visit summaries")
            insert_visit_summaries(session, visits_all)
    finally:
        session.close()
        print(f"[etl] Pipeline for {portal_name} complete")
