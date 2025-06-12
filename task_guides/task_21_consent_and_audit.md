# Task 21: Consent UX and Audit Logging

## 🎯 Goal
Ensure users explicitly authorize portal access and actions are logged for transparency and compliance.

## 📂 Target Files
- `app/api/consent.py`
- `app/storage/audit.py`

## 📋 Instructions
- Create `POST /consent` endpoint (FastAPI)
  - Input: user_id, portal_name, action (e.g. "scrape"), timestamp
  - Store to consent log
- Create audit log helper:
  - `log_event(user, action, context)` to JSON file or encrypted DB
- Consent request UI should simulate:
  > "May I log into your MyChart account to check for new lab results?"
  - Record confirmation before automation begins

## 🧪 Test
- Unit test for logging module
- Mock consent capture and verify file/db writes

## ✅ What to Report Back
- Consent flow (stubbed or real)
- Audit log format
- Example log entries