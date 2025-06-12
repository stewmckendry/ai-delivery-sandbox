# Codex Agent Task: Pipeline Orchestrator

## 🎯 Goal
Tie together scraping, parsing, structuring, and DB writing into a unified ETL pipeline.

## 📂 Target File
- `app/orchestrator.py`

## 📋 Instructions
- Define `run_etl_for_portal(portal_name: str)`
- Look up scraper function in `app/adapters/<portal_name>.py`
- Scrape and save raw files (HTML, PDFs)
- Parse files using appropriate parser from `app/processors/`
- Save parsed structured data to DB via `insert_lab_results()` / `insert_visit_summaries()`
- Log each step to console

## 🧪 Test
- Add `tests/test_orchestrator.py`
- Mock scraper + parser functions
- Confirm that DB was called and records were inserted

## 🔄 Reuse
- All existing scraper, parser, and structuring modules
- DB setup via `storage/db.py`

## ✅ What to Report Back
- `orchestrator.py` with full pipeline logic
- Test case with mocked scraper/parser
- Sample log output showing ETL sequence

Refer to `task_guides/review_checklist.md` for structure.