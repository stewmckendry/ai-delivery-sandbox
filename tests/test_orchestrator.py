import os
def test_run_etl_for_portal(monkeypatch, tmp_path, capsys):
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["PORTAL_A_USERNAME"] = "user"
    os.environ["PORTAL_A_PASSWORD"] = "pass"

    html_file = tmp_path / "dash.html"
    html_file.write_text("<div class='visit'><span class='date'>2023-01-01</span><span class='provider'>Clinic</span><span class='doctor'>Dr. X</span><p class='notes'>Hi</p></div>")
    pdf_file = tmp_path / "lab.pdf"
    pdf_file.write_bytes(b"%PDF-1.4")

    # Mock scraper
    def fake_scraper(username, password):
        assert username == "user"
        assert password == "pass"
        return {"files": [str(html_file), str(pdf_file)]}

    import app.adapters.portal_a as portal_module
    monkeypatch.setattr(portal_module, "scrape_portal_a", fake_scraper)

    # Mock parsers
    visits = [{"date": "2023-01-01", "provider": "Clinic", "doctor": "Dr. X", "notes": "Hi"}]
    labs = [{"test_name": "A", "value": "1", "units": "mg", "date": "2023-01-02"}]

    import app.processors.visit_html_parser as vh_parser
    import app.processors.lab_pdf_parser as lab_parser
    monkeypatch.setattr(vh_parser, "extract_visit_summaries", lambda html: visits)
    monkeypatch.setattr(lab_parser, "extract_lab_results_with_date", lambda path: labs)

    inserted = {"labs": None, "visits": None}
    import app.processors.structuring as struct_module

    def fake_insert_labs(session, results):
        inserted["labs"] = results

    def fake_insert_visits(session, results):
        inserted["visits"] = results

    monkeypatch.setattr(struct_module, "insert_lab_results", fake_insert_labs)
    monkeypatch.setattr(struct_module, "insert_visit_summaries", fake_insert_visits)

    from app.orchestrator import run_etl_for_portal
    run_etl_for_portal("portal_a")

    assert inserted["labs"] == labs
    assert inserted["visits"] == visits

    captured = capsys.readouterr()
    assert "Starting pipeline for portal_a" in captured.out
    assert "Pipeline for portal_a complete" in captured.out
