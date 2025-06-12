# Task 20 Review: Secure Credential Fetch in Orchestrator

## ✅ Summary
`run_etl_for_portal()` is now credential-aware. It securely retrieves credentials, passes them to the appropriate scraper, and deletes them post-use. All key actions are logged.

## 📂 Files
- `app/orchestrator.py`
- `tests/test_orchestrator.py`

## 🔐 Behavior
- 🟢 Fetches encrypted credentials using `get_credentials()`
- 🟢 Scraper supports dynamic `username`, `password` injection
- 🟢 Deletes credentials after use
- 🟢 Logs all major stages: credential presence, usage, deletion

## 🧪 Test
```bash
pytest -k orchestrator -q
```
- ✅ Mocks all credential functions
- ✅ Asserts credential fetch, use, and deletion
- ✅ Verifies console logs

## 🔄 Reuse
- Integrates with Task 19's `credentials.py`
- Compatible with existing scraper and parser structure

## 💬 Feedback
- ✅ Credentials passed securely, no hardcoding
- ✅ Exception-safe deletion with clear audit logs
- ✅ Ready to support real-world inputs from UI stub

## 🚀 ETL now production-like: credential-based, secure, and logged