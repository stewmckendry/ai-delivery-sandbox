# Codex Agent Task: Secure Orchestrator with Credential Fetch

## 🎯 Goal
Update the ETL orchestrator to fetch and use user-submitted credentials securely.

## 📂 Target File
- `app/orchestrator.py`

## 📋 Instructions
- Modify `run_etl_for_portal()`:
  - Before scraper call, fetch credentials using `get_credentials(portal)` from `credentials.py`
  - Pass username and password into scraper function if supported
  - After scrape, immediately call `delete_credentials(portal)`
  - Add logs for access, success, or expiry

## 🔄 Reuse
- `app/storage/credentials.py` from Task 19
- Scraper modules in `app/adapters/`

## 🧪 Test
- Modify `tests/test_orchestrator.py` to mock credential functions
- Simulate full cycle with logs

## ✅ What to Report Back
- Updated orchestrator
- Logs showing secure fetch/use
- Updated tests

Refer to `AGENTS.md` and `review_checklist.md` for structure.