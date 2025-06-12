# Codex Agent Task: End-to-End Test Runner

## 🎯 Goal
Simulate the full pipeline and show outputs at each stage for QA and traceability.

## 📂 Target File
- `scripts/e2e_test_runner.py`

## 📋 Instructions
- Simulate the following:
  - Mock portal scrape (reuse static sample file)
  - Parse sample files (PDFs/HTML)
  - Insert records into in-memory SQLite
  - Call `summarize_lab_results()`
  - Call `/ask` endpoint locally with FastAPI TestClient
- Print outputs at each stage with labeled headers

## 🧪 Test
- No separate test — output should include clear trace
- Script should exit non-zero on failure

## 🔄 Reuse
- `app/orchestrator.py`, `summarizer.py`, `rag.py`
- Static test files for mock data

## ✅ What to Report Back
- Script and sample terminal output
- Notes on any stages skipped or mocked

Refer to `task_guides/review_checklist.md` for structure.