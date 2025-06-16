# Task 209: End-to-End Test Plan (Operator Upload → RAG)

## 🎯 Goal
Verify the complete user flow from Operator-assisted data collection to usable structured health records available via /ask, /export, and /status endpoints.

---

## 🧪 Test Steps

### 1. Operator File Collection
- Log in and collect data from a test portal (e.g., Strava, LifeLabs)
- Save the page as HTML or use site’s print-to-PDF feature
- Verify files show real data (open locally)

### 2. Upload to Azure Blob
- Use the `/upload` form and session key (e.g., `test_user`)
- Upload one or more `.html` or `.pdf` files
- Confirm upload logs appear in audit log

### 3. Trigger ETL
- Call `/process?session_key=test_user` (or `/status` prompt → POST `/process`)
- Confirm output:
  - Records parsed from HTML or PDF
  - Summary written to logs/blob_runs/
  - Structured records inserted into DB

### 4. Query Data (/ask)
- Run `python scripts/ask_tool.py --query "What are my latest test results?"`
- Validate that output includes records from uploaded file

### 5. Export Data (/export)
- Run:
```bash
python scripts/export_records.py --db health_data.db --format markdown --output out.md
```
- Confirm exported file includes visit, lab, or structured content

### 6. Check Status (/status)
- Call `/status?session_key=test_user`
- Confirm:
  - Record counts match ETL
  - Timestamps are recent

---

## ✅ What to Report Back
- Which files were tested (HTML, PDF)
- Summary output + sample ask/export results
- Any ETL failures or skipped records

This validates that Operator-extracted files are usable in our end-to-end pipeline.