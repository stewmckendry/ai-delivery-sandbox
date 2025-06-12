# Task 31: Create Test Portal Adapter for Pipeline QA

## 🎯 Goal
Implement a Playwright-compatible `test_portal` adapter that generates mock HTML + PDF content for full pipeline test runs (no login).

## 📂 Target File
- `app/adapters/test_portal.py`

## 📋 Instructions
- Simulate login using a static HTML file with test credentials from `.env`
- Generate a few pages:
  - Page 1: Link to lab results (PDF)
  - Page 2: Embedded visit summary (HTML)
- Save content to `/tmp/` with unique filenames
- Return metadata and file paths for processing by orchestrator

## 🧪 Test
- Run via:
```bash
python scripts/run_portal_test.py --portal test_portal --debug
```
- Confirm:
  - Structured JSON output
  - Audit logs
  - Screenshots (if challenge simulated)

## ✅ What to Report Back
- Adapter logic
- Sample test artifacts (HTML, PDF, log, summary)
- Any assumptions about page structure

Refer to Task 28 + README for test pipeline integration.