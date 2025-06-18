# ✅ Task 303: End-to-End Testing of FastAPI on Railway

## 🎯 Goal
Verify that the cloud-hosted FastAPI app on Railway functions correctly for the full user flow from Operator upload to record querying and exporting.

Codex Agent should run the tests described below and record results. Use the deployed Railway URL.

---

## 🌐 Railway URL
```
https://ai-delivery-sandbox-production-d1a7.up.railway.app
```

---

## 🧪 Test Steps
Adapted from `task_209_end_to_end_test_plan.md`

### 1. Start Session
```bash
curl https://ai-delivery-sandbox-production-d1a7.up.railway.app/session
```
Use the returned `session_key` for the following steps.

### 2. File Collection
 - ✅ Save `.html` or `.pdf` file exported from a health portal
 - ✅ Inspect locally to confirm content integrity

### 3. Upload via Web Interface
Open:
```
https://ai-delivery-sandbox-production-d1a7.up.railway.app/upload?session=<key>&portal=strava
```
 - ✅ Drag and drop or select file to upload
 - ✅ Confirm success message "Uploaded <filename>"
 - ✅ Metadata is logged automatically

### 4. Trigger ETL via Railway
```bash
curl -X POST https://ai-delivery-sandbox-production-d1a7.up.railway.app/process -F session_key=<key>
```
- ✅ Logs show extraction and DB insertion

### 5. Ask Question
```bash
curl -X POST https://ai-delivery-sandbox-production-d1a7.up.railway.app/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What are my latest test results?", "session_key": "<key>"}'
```
- ✅ Response includes extracted record content

### 6. Export Data via API
Markdown:
```bash
curl "https://ai-delivery-sandbox-production-d1a7.up.railway.app/export?session_key=<key>&format=markdown"
```
JSON:
```bash
curl "https://ai-delivery-sandbox-production-d1a7.up.railway.app/export?session_key=<key>&format=json"
```
PDF:
```bash
curl -o records.pdf "https://ai-delivery-sandbox-production-d1a7.up.railway.app/export?session_key=<key>&format=pdf"
```
- ✅ Outputs match uploaded file and extracted data

### 7. Check Status
```bash
curl https://ai-delivery-sandbox-production-d1a7.up.railway.app/summary?session_key=<key> | jq
```
- ✅ Confirm structured counts, timestamps, and sources

---

## ✅ Done When
- `/upload`, `/process`, `/ask`, `/export`, and `/summary` all work via Railway
- Responses reflect uploaded file content
- Agent provides sample output and issues if any