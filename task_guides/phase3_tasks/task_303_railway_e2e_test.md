# ✅ Task 303: End-to-End Testing of FastAPI on Railway

## 🎯 Goal
Verify that the cloud-hosted FastAPI app on Railway functions correctly for the full user flow from Operator upload to record querying and exporting.

Codex Agent should run the tests described below and record results. Use the deployed Railway URL instead of localhost.

---

## 🌐 Railway URL
```
https://<your-app>.up.railway.app
```

---

## 🧪 Test Steps
Adapted from `task_209_end_to_end_test_plan.md`

### 1. File Collection
- ✅ Save `.html` or `.pdf` file exported from health portal
- ✅ Inspect locally to confirm content integrity

### 2. Upload to Azure Blob via CLI
```bash
python scripts/upload_to_blob.py --session-key test_user --file path/to/file.html --portal strava
```
- ✅ Confirm CLI says "Uploaded"
- ✅ Check `/summary?session_key=test_user` on Railway for new file

### 3. Trigger ETL via Railway
```bash
curl -X POST https://<your-app>.up.railway.app/process -F session_key=test_user
```
- ✅ Confirm logs show extraction and insertion
- ✅ Optional: check `logs/blob_runs/` locally if mounted

### 4. Ask Question
```bash
curl -X POST https://<your-app>.up.railway.app/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What are my latest test results?", "session_key": "test_user"}'
```
- ✅ Response includes lab results, visits, or structured data

### 5. Export (optional)
```bash
python scripts/export_records.py --db health_data.db --format markdown --output out.md
```
- ✅ Output reflects uploaded file content

### 6. Status Check
```bash
curl https://<your-app>.up.railway.app/summary?session_key=test_user | jq
```
- ✅ Confirm counts and timestamps are accurate

---

## ✅ Done When
- `/ask`, `/summary`, and `/process` work via Railway URL
- Structured content reflects uploaded file
- Agent shares output samples and any errors

Include in final report:
- What file was used
- Output from `/ask` and `/summary`
- Any functional gaps or failures
