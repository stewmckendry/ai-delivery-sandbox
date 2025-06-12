# Task 15 Review: Orchestrator Pipeline

## ✅ Summary
Implements `run_etl_for_portal()` to:
- Dynamically import and invoke portal-specific scraper
- Read and save all scraped files
- Parse content with lab or visit extractors
- Store structured results into SQLite via SQLAlchemy
- Log each phase of the ETL flow

## 📂 Files Created
- `app/orchestrator.py`
- `tests/test_orchestrator.py`

## 🧪 Unit Test
- Mocks:
  - Scraper return values
  - HTML + PDF parsers
  - Insert functions
- Uses in-memory SQLite and asserts calls/logs

To run:
```bash
PYTHONPATH=$PWD pytest -q tests/test_orchestrator.py
```

## 🔁 Reuse
- Parsers: `lab_pdf_parser`, `visit_html_parser`
- Insert logic: `insert_lab_results`, `insert_visit_summaries`
- Storage: `save_file`

## 💬 Feedback
- ✅ Elegant dynamic module loader for scraper
- ✅ Clean branching on file type for dispatch
- ✅ End-to-end validated with mocks
- 🟡 Optional future: isolate DB transaction scope per file

## 🚀 Ready to support full data ingestion for a portal