import os
import logging
from pathlib import Path
import sys
import importlib

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def create_sample_pdf(path: Path) -> None:
    import fitz

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Cholesterol 5.8 mmol/L 2023-05-01")
    doc.save(path)
    doc.close()


def test_run_etl_from_blobs(monkeypatch, tmp_path, caplog):
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"

    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    monkeypatch.setenv("FERNET_KEY", key.decode())

    if "app.orchestrator" in sys.modules:
        del sys.modules["app.orchestrator"]

    import app.storage.blob as blob_module

    html_file = tmp_path / "visit.html"
    html_file.write_text(
        "<div class='visit'><span class='date'>2023-01-01</span><span class='provider'>Clinic</span><span class='doctor'>Dr. X</span><p class='notes'>Hi</p></div>"
    )
    pdf_file = tmp_path / "lab.pdf"
    create_sample_pdf(pdf_file)
    txt_file = tmp_path / "misc.txt"
    txt_file.write_text("Random note text")

    prefix = "user/session"

    monkeypatch.setattr(
        blob_module,
        "list_blobs",
        lambda p: [f"{prefix}/visit.html", f"{prefix}/lab.pdf", f"{prefix}/misc.txt"],
    )
    monkeypatch.setattr(
        blob_module,
        "download_blob",
        lambda name: html_file.read_bytes()
        if name.endswith("html")
        else pdf_file.read_bytes()
        if name.endswith("pdf")
        else txt_file.read_bytes(),
    )
    monkeypatch.setattr(blob_module, "delete_blob", lambda name: None)

    inserted = {"records": None, "labs": None, "visits": None, "fhir": None}

    import app.storage.structured as structured_module
    import app.extractor as extractor_module
    import app.cleaner as cleaner_module
    import app.prompts.summarizer as summarizer_module
    import app.processors.structuring as struct_module

    monkeypatch.setattr(
        structured_module,
        "insert_structured_records",
        lambda s, r, session_key=None: inserted.update({"records": r, "session": session_key})
    )
    original_insert_lab = struct_module.insert_lab_results
    def wrap_lab(s, r, session_key=None):
        inserted.update({"labs": r})
        return original_insert_lab(s, r, session_key=session_key)
    monkeypatch.setattr(struct_module, "insert_lab_results", wrap_lab)

    original_insert_visit = struct_module.insert_visit_summaries
    def wrap_visit(s, r, session_key=None):
        inserted.update({"visits": r})
        return original_insert_visit(s, r, session_key=session_key)
    monkeypatch.setattr(struct_module, "insert_visit_summaries", wrap_visit)

    def _record_fhir(s, r):
        if inserted.get("fhir") is None:
            inserted["fhir"] = []
        inserted["fhir"].extend(r)

    monkeypatch.setattr(struct_module, "insert_fhir_resources", _record_fhir)

    def fake_extract(text, src, **_k):
        if src.endswith("visit.html"):
            return [{"type": "", "text": "Metformin 500 mg daily", "source_url": src}]
        if src.endswith("lab.pdf"):
            return [{"type": "", "text": "Patient has diabetes", "source_url": src}]
        return [{"type": "", "text": "Allergic to penicillin", "source_url": src}]

    monkeypatch.setattr(extractor_module, "extract_relevant_content", fake_extract)
    monkeypatch.setattr(cleaner_module, "clean_blocks", lambda blocks, **k: [b["text"] for b in blocks])
    monkeypatch.setattr(summarizer_module, "summarize_database_records", lambda s: "Blob summary")

    orch_module = importlib.import_module("app.orchestrator")
    importlib.reload(orch_module)
    def fake_chat(messages, **_kwargs):
        text = messages[0]["content"]
        if "Metformin" in text:
            return '{"clinical_type": "MedicationStatement", "code": "860975", "code_system": "RxNorm", "display": "Metformin"}'
        if "diabetes" in text:
            return '{"clinical_type": "Condition", "code": "44054006", "code_system": "SNOMED", "display": "Diabetes mellitus"}'
        if "penicillin" in text:
            return '{"clinical_type": "AllergyIntolerance"}'
        return '{}'

    monkeypatch.setattr(orch_module, "chat_completion", fake_chat)
    monkeypatch.setattr(orch_module, "_detect_labs_and_visits_with_llm", lambda recs: ([{"test_name": "Cholesterol", "value": "5.8", "units": "mmol/L", "date": "2023-05-01"}], [{"date": "2023-06-01", "provider": "Clinic", "doctor": "Dr. X", "notes": "Hi"}]))
    monkeypatch.setattr(orch_module, "_annotate_labs_with_llm", lambda labs: [{"test_name": "Cholesterol", "value": "5.8", "units": "mmol/L", "date": "2023-05-01", "loinc_code": "2093-3", "fhir": {"resourceType": "Observation"}}])
    monkeypatch.setattr(orch_module, "_annotate_visits_with_llm", lambda visits: [{"date": "2023-06-01", "provider": "Clinic", "doctor": "Dr. X", "notes": "Hi", "snomed_code": "308335008", "fhir": {"resourceType": "Encounter"}}])
    from app.orchestrator import run_etl_from_blobs

    caplog.set_level(logging.INFO)
    summary = run_etl_from_blobs(prefix)

    assert inserted["records"] and len(inserted["records"]) == 3
    assert inserted["session"] == prefix
    assert all(r["source"] == "operator" for r in inserted["records"])
    types = {r.get("clinical_type") for r in inserted["records"]}
    assert "MedicationStatement" in types
    assert "Condition" in types
    assert "AllergyIntolerance" in types

    assert inserted["labs"] and inserted["labs"][0]["loinc_code"] == "2093-3"
    assert inserted["visits"] and inserted["visits"][0]["snomed_code"] == "308335008"
    assert inserted["fhir"] and len(inserted["fhir"]) == 2

    summary_file = Path("logs/blob_runs/user_session_summary.md")
    assert not summary_file.exists()
    assert summary == "Blob summary"

    importlib.reload(orch_module)

