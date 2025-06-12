# Task 30: Hook Consent + Audit into ETL Pipeline

## 🎯 Goal
Log explicit user consent and audit major ETL actions for transparency and compliance.

## 📂 Files
- `app/orchestrator.py`
- `app/storage/audit.py`

## 📋 Instructions
- At start of `run_etl_for_portal()`:
  - Call `log_event(user, "consent_granted", {"portal": ..., "timestamp": ...})`
  - Make `user_id` an argument or environment variable
- At major checkpoints (login, scrape, parse, insert):
  - Call `log_event(user, action, context)`
  - Context should include portal name and action metadata
- Optionally: invoke `POST /consent` if HTTP is available

## 🧪 Test
- Run with `--portal test_portal`
- Inspect `data/audit_log.json`

## ✅ What to Report Back
- Audit logs from a test run
- Any refactor needed to pass user_id contextfully

Refer to Task 21 review for audit expectations.