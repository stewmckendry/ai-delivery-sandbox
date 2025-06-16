# Task 209: End-to-End Test Plan (Operator Upload → RAG)

## 🎯 Goal
Verify the complete user flow from Operator-assisted data collection to usable structured health records available via `/ask`, `/export`, and `/status` endpoints.

---

## 🧪 Test Steps

### 1. Operator File Collection
**Pre:** Ensure Operator is running, and you are logged into a test portal (e.g., Strava, LifeLabs)

- ✅ Open desired record (lab result, activity log, etc.)
- ✅ Use **Save Page As** for HTML or portal’s **Print to PDF**
- ✅ Save file with a clear name (e.g., `strava_activity_2025-06-16.html`)
- ✅ Inspect file locally to confirm content

### 2. Upload to Azure Blob
**Pre:** Ensure `.env` has correct `AZURE_STORAGE_CONNECTION_STRING`

- ✅ Open `http://localhost:8000/upload?session=test_user`
- ✅ Upload the saved `.html` or `.pdf` file(s)
- ✅ Confirm UI shows "Uploaded"

**Post:** Confirm log entry is created
- Check `audit.json` for action `file_upload`

### 3. Trigger ETL
**Option A:** From browser prompt
- Visit `/status?session_key=test_user`
- Accept prompt to process

**Option B:** Manually run
```bash
curl -X POST http://localhost:8000/process -F session_key=test_user
```

**Post:**
- Check logs: `logs/blob_runs/test_user_summary.md`
- Verify `health_data.db` is updated

### 4. Query Data (/ask)
```bash
python scripts/ask_tool.py --query "What are my latest test results?" --db health_data.db
```
**Post:** Confirm relevant content appears from uploaded file

### 5. Export Data (/export)
```bash
python scripts/export_records.py --db health_data.db --format markdown --output out.md
```
**Post:** Open `out.md` and confirm structured export

### 6. Check Status (/status)
```bash
curl http://localhost:8000/status?session_key=test_user | jq
```
**Post:**
- Validate counts (labs, visits, structured)
- Confirm `latest_upload` and `latest_processing` are recent

---

## ✅ What to Report Back
- Which files tested (`.html`, `.pdf`)
- Output examples from `/ask`, `/export`, `/status`
- Any failed extractions or content gaps

This confirms Operator-exported files are fully usable within the app pipeline.