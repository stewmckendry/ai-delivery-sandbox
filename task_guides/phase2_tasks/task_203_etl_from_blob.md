# Task 203: Run ETL from Azure Blob Uploads

## 🎯 Goal
Extend the current ETL pipeline to ingest and process user-uploaded files from Azure Blob.

## 📂 Context
This is part of Phase 2 - refer to phase2_operator_architecture.md for overall architecture.  We are replacing the portal scraping with OpenAI Operator to streamline data retrieval.

## 📂 Target Files
- `app/orchestrator.py`
- `app/storage/blob.py`
- `scripts/run_etl_from_blob.py` (new CLI)

## 📋 Instructions
- Load file(s) from Blob (path or prefix)
- Parse contents based on format:
  - PDF → labs
  - HTML → visits
  - Text → structured or billing
- Reuse existing extraction + structuring
- Call summarizer if records inserted

## 🔐 Security Notes
- Sanitize filenames
- Only read blobs from `user_id/session_id` container
- Cleanup after parse (optional)

## 🧪 Test
- Upload 1 visit + 1 lab via Task 201
- Confirm records appear in DB
- Confirm summary generated

## ✅ What to Report Back
- Example blob input → summary output
- Record counts per type
- CLI usage (if added)

This connects uploaded data with our structured health record system.