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

    prefix = "user/session"

    monkeypatch.setattr(blob_module, "list_blobs", lambda p: [f"{prefix}/visit.html", f"{prefix}/lab.pdf"])
    monkeypatch.setattr(blob_module, "download_blob", lambda name: html_file.read_bytes() if name.endswith("html") else pdf_file.read_bytes())
    monkeypatch.setattr(blob_module, "delete_blob", lambda name: None)

    visits = [{"date": "2023-01-01", "provider": "Clinic", "doctor": "Dr. X", "notes": "Hi"}]
    labs = [{"test_name": "A", "value": "1", "units": "mg", "date": "2023-01-02"}]

    import app.processors.visit_html_parser as vh_parser
    import app.processors.lab_pdf_parser as lab_parser
    import app.processors.structuring as struct_module
    import app.storage.structured as structured_module
    import app.crawler as crawler_module
    import app.extractor as extractor_module
    import app.cleaner as cleaner_module
    import app.prompts.summarizer as summarizer_module

    monkeypatch.setattr(vh_parser, "extract_visit_summaries", lambda h: visits)
    monkeypatch.setattr(lab_parser, "extract_lab_results_with_date", lambda p: labs)

    inserted = {"labs": None, "visits": None, "records": None}

    monkeypatch.setattr(struct_module, "insert_lab_results", lambda s, r: inserted.update({"labs": r}))
    monkeypatch.setattr(struct_module, "insert_visit_summaries", lambda s, r: inserted.update({"visits": r}))
    monkeypatch.setattr(structured_module, "insert_structured_records", lambda s, r: inserted.update({"records": r}))

    monkeypatch.setattr(extractor_module, "extract_relevant_content", lambda html, src, **k: [{"type": "visit_note", "text": "note", "source_url": src}])
    monkeypatch.setattr(cleaner_module, "clean_blocks", lambda blocks, **k: [b["text"] for b in blocks])
    monkeypatch.setattr(crawler_module, "crawl_portal", lambda *a, **k: ([], set()))
    monkeypatch.setattr(summarizer_module, "summarize_database_records", lambda s: "Blob summary")

    orch_module = importlib.import_module("app.orchestrator")
    importlib.reload(orch_module)
    from app.orchestrator import run_etl_from_blobs

    caplog.set_level(logging.INFO)
    run_etl_from_blobs(prefix)

    assert inserted["labs"] == labs
    assert inserted["visits"] == visits
    assert inserted["records"] and len(inserted["records"]) > 0

    summary_file = Path("logs/blob_runs/user_session_summary.md")
    assert summary_file.exists()
    assert "Blob summary" in summary_file.read_text()

    importlib.reload(orch_module)
