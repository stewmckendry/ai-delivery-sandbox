# Task 30 Review: Consent + Audit Logging in ETL

## ✅ Summary
`run_etl_for_portal()` now logs user consent and records all major pipeline events (login, scrape, parse, insert) to the audit file.

## 📂 File
- `app/orchestrator.py`

## ✅ Audit Points Logged
- Consent granted (user ID, portal, timestamp)
- Credential-based login attempt
- File scraping and count
- Parsing summary (file count, labs, visits)
- Insert summary (labs + visits)

## 📄 Audit Format
```json
{
  "timestamp": "...",
  "user": "etl_user",
  "action": "scrape",
  "context": {
    "portal": "test_portal",
    "file_count": 2
  }
}
```

## 🧪 Test
```bash
pytest -q
python scripts/run_portal_test.py --portal test_portal --depth 1 --debug
```
- ✅ Confirms audit file written
- ❌ LLM failure due to OpenAI key missing (non-blocking for audit)

## 💬 Feedback
- ✅ Logs are detailed and timestamped
- ✅ Tracks full pipeline journey for post-hoc review or compliance
- 🟡 Future: add audit replay viewer or consent status tracker

## 🚀 ETL now has full observability from user approval to insert confirmation