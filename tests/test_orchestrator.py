import os
import logging
from pathlib import Path


def test_run_etl_for_portal(monkeypatch, tmp_path, caplog):
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"

    html_file = tmp_path / "dash.html"
    html_file.write_text(
        "<div class='visit'><span class='date'>2023-01-01</span><span class='provider'>Clinic</span><span class='doctor'>Dr. X</span><p class='notes'>Hi</p></div>"
    )
    pdf_file = tmp_path / "lab.pdf"
    pdf_file.write_bytes(b"%PDF-1.4")

    # Mock credential retrieval
    from cryptography.fernet import Fernet

    key = Fernet.generate_key()
    monkeypatch.setenv("FERNET_KEY", key.decode())
    import importlib
    import app.orchestrator as orch_module
    importlib.reload(orch_module)
    import app.storage.credentials as cred_module

    monkeypatch.setattr(
        cred_module,
        "get_credentials",
        lambda portal: {"username": "user", "password": "pass"},
    )
    deleted = {"called": False}

    def fake_delete(portal):
        deleted["called"] = True

    monkeypatch.setattr(cred_module, "delete_credentials", fake_delete)

    # Mock scraper
    def fake_scraper(username, password):
        assert username == "user"
        assert password == "pass"
        return {"files": [str(html_file), str(pdf_file)]}

    import app.adapters.portal_a as portal_module

    monkeypatch.setattr(portal_module, "scrape_portal_a", fake_scraper)

    # Mock parsers
    visits = [
        {"date": "2023-01-01", "provider": "Clinic", "doctor": "Dr. X", "notes": "Hi"}
    ]
    labs = [{"test_name": "A", "value": "1", "units": "mg", "date": "2023-01-02"}]

    import app.processors.visit_html_parser as vh_parser
    import app.processors.lab_pdf_parser as lab_parser

    monkeypatch.setattr(vh_parser, "extract_visit_summaries", lambda html: visits)
    monkeypatch.setattr(lab_parser, "extract_lab_results_with_date", lambda path: labs)

    inserted = {"labs": None, "visits": None}
    import app.processors.structuring as struct_module
    import app.storage.structured as structured_module

    def fake_insert_labs(session, results):
        inserted["labs"] = results

    def fake_insert_visits(session, results):
        inserted["visits"] = results

    structured = {"records": None}
    monkeypatch.setattr(struct_module, "insert_lab_results", fake_insert_labs)
    monkeypatch.setattr(struct_module, "insert_visit_summaries", fake_insert_visits)
    monkeypatch.setattr(structured_module, "insert_structured_records", lambda s, r: structured.update({"records": r}))

    # Mock AI modules
    import app.crawler as crawler_module
    import app.extractor as extractor_module
    import app.cleaner as cleaner_module

    called = {"crawl": False, "extract": 0}

    def fake_crawl(html, base_url, fetch, limit=3):
        called["crawl"] = True
        return ([{"url": str(html_file), "html": html_file.read_text()}], {str(html_file)})

    def fake_extract(html, src, max_chunk_chars=4000):
        called["extract"] += 1
        return [{"type": "visit_note", "text": "hello", "source_url": src}]

    monkeypatch.setattr(crawler_module, "crawl_portal", fake_crawl)
    monkeypatch.setattr(extractor_module, "extract_relevant_content", fake_extract)
    monkeypatch.setattr(cleaner_module, "clean_blocks", lambda blocks, **k: [b["text"] for b in blocks])

    import app.prompts.summarizer as summarizer_module
    monkeypatch.setattr(summarizer_module, "summarize_database_records", lambda s: "Run summary")
    import importlib
    import app.orchestrator as orch_module
    importlib.reload(orch_module)
    from app.orchestrator import run_etl_for_portal

    caplog.set_level(logging.INFO)
    run_etl_for_portal("portal_a")

    assert deleted["called"] is True

    assert called["crawl"] is True
    assert called["extract"] > 0

    assert inserted["labs"] == labs
    assert inserted["visits"] == visits
    assert structured["records"] and len(structured["records"]) > 0

    summary_file = Path("logs/portal_runs/portal_a_summary.md")
    assert summary_file.exists()
    assert "Run summary" in summary_file.read_text()

    logs = caplog.text
    assert "Starting pipeline for portal_a" in logs
    assert "Retrieving credentials for portal_a" in logs
    assert "Credentials found for portal_a" in logs
    assert "Deleted credentials for portal_a" in logs
    assert "Pipeline for portal_a complete" in logs

def test_orchestrator_handles_challenge(monkeypatch, tmp_path, caplog):
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"

    html_file = tmp_path / "dash.html"
    html_file.write_text(
        "<div class='visit'><span class='date'>2023-01-01</span>"
        "<span class='provider'>Clinic</span><span class='doctor'>Dr. Y" \
        "</span><p class='notes'>Hi</p></div>"
    )

    pdf_file = tmp_path / "lab.pdf"
    pdf_file.write_bytes(b"%PDF-1.4")

    from cryptography.fernet import Fernet

    key = Fernet.generate_key()
    monkeypatch.setenv("FERNET_KEY", key.decode())
    import importlib
    import app.orchestrator as orch_module
    importlib.reload(orch_module)
    import app.storage.credentials as cred_module

    monkeypatch.setattr(
        cred_module,
        "get_credentials",
        lambda portal: {"username": "user", "password": "pass"},
    )
    monkeypatch.setattr(cred_module, "delete_credentials", lambda p: None)

    # fake challenge flow
    from app.adapters.common import challenges as ch_module

    async def fake_await(cid):
        return "code"

    monkeypatch.setattr(ch_module, "_await_response", fake_await)

    def fake_scraper(username, password):
        assert username == "user"
        assert password == "pass"

        def resume(code):
            assert code == "code"
            return {"files": [str(html_file), str(pdf_file)]}

        return {"challenge_id": "cid", "resume": resume}

    import app.adapters.portal_a as portal_module

    monkeypatch.setattr(portal_module, "scrape_portal_a", fake_scraper)

    visits = [
        {"date": "2023-01-01", "provider": "Clinic", "doctor": "Dr. Y", "notes": "Hi"}
    ]
    labs = [{"test_name": "A", "value": "1", "units": "mg", "date": "2023-01-02"}]

    import app.processors.visit_html_parser as vh_parser
    import app.processors.lab_pdf_parser as lab_parser

    monkeypatch.setattr(vh_parser, "extract_visit_summaries", lambda html: visits)
    monkeypatch.setattr(lab_parser, "extract_lab_results_with_date", lambda p: labs)

    import app.processors.structuring as struct_module
    import app.storage.structured as structured_module

    monkeypatch.setattr(struct_module, "insert_lab_results", lambda s, r: None)
    monkeypatch.setattr(struct_module, "insert_visit_summaries", lambda s, r: None)
    monkeypatch.setattr(structured_module, "insert_structured_records", lambda s, r: None)

    import app.crawler as crawler_module
    import app.extractor as extractor_module
    import app.cleaner as cleaner_module

    monkeypatch.setattr(crawler_module, "crawl_portal", lambda *a, **k: ([{"url": str(html_file), "html": html_file.read_text()}], {str(html_file)}))
    monkeypatch.setattr(extractor_module, "extract_relevant_content", lambda html, src, **k: [{"type": "visit_note", "text": "hello", "source_url": src}])
    monkeypatch.setattr(cleaner_module, "clean_blocks", lambda blocks, **k: [b["text"] for b in blocks])

    import app.prompts.summarizer as summarizer_module
    monkeypatch.setattr(summarizer_module, "summarize_database_records", lambda s: "Run summary")
    import importlib
    import app.orchestrator as orch_module
    importlib.reload(orch_module)
    from app.orchestrator import run_etl_for_portal

    caplog.set_level(logging.INFO)
    run_etl_for_portal("portal_a")

    logs = caplog.text
    assert "Waiting for challenge cid" in logs
    assert "Resuming challenge cid" in logs
    summary_file = Path("logs/portal_runs/portal_a_summary.md")
    assert summary_file.exists()
    assert "Run summary" in summary_file.read_text()
