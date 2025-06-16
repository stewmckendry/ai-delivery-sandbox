# Task 205: Status Route (/status)

## 🎯 Goal
Provide users with visibility into what health data is stored, when it was uploaded, and from which portals.

## 📂 Context
This is part of Phase 2 - refer to phase2_operator_architecture.md for overall architecture.  We are replacing the portal scraping with OpenAI Operator to streamline data retrieval.

## 📂 Target Files
- `app/api/status.py` (new)
- `app/storage/db.py`
- `app/storage/models.py`

## 📋 Instructions
- Add new route `/status?session_key=xyz`
- Return:
  - List of uploaded files (from `audit` log or `uploads` table)
  - Detected portals, record types (labs, visits), and counts
  - Timestamps of latest uploads and processing
- Optionally: link to `upload_form` or `process` route if no records found

## 🧪 Test
- Upload and process a few files
- Query `/status?session_key=test_user`
- Confirm correct file counts, types, and timestamps

## ✅ What to Report Back
- Sample JSON output
- Example log data
- Suggestions to user if nothing is stored yet

This lets users audit and understand what data is available for Q&A.