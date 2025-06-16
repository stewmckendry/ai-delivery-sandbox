# Task 204: Consent and Confirm Before ETL

## 🎯 Goal
Add a clear user-facing prompt to confirm before processing uploaded files. This ensures consent is explicit and logged before any health data analysis occurs.

## 📂 Target Files
- `app/api/etl.py` (new)
- `app/storage/audit.py`

## 📋 Instructions
- Add new route `/process` that:
  - Accepts `session_key` as input
  - Returns a confirmation prompt: "You uploaded X files. Do you want to process them now?"
  - On POST with confirmation, logs consent
  - Calls ETL pipeline (`run_etl_from_blob(session_key)`)

## 🔐 Notes
- Log consent to `audit.log_event(session_key, "consent_given", {timestamp})`
- Support dry-run mode for dev

## 🧪 Test
- Upload file
- Visit `/process?session_key=abc`
- Confirm and check logs
- Verify records added to DB after ETL

## ✅ What to Report Back
- Confirmation message UX
- Consent audit log
- Example ETL output from confirmed session

This task ensures responsible handling of uploaded health records.