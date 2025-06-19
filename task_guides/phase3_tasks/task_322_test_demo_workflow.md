# ✅ Task 322: Test Demo Workflow via `/load_demo` and Downstream Tools

## 🧠 Context
Demo tooling has been implemented to support frictionless onboarding and test flows. The repo is `ai-delivery-sandbox`, branch `sandbox-curious-fox`.
This task validates the full end-to-end path using `/load_demo` + `/ask_vector`, `/summary`, `/export`, etc.

## 🎯 Goal
Confirm the demo session flow works via CLI and GPT using cloud endpoints.

## 🧪 Test Plan

### 1. **Prepare Demo Files**
Ensure these demo files exist locally in `project/demo_data/`:
- `lab_results.pdf`
- `family_doctor_visit.pdf`
- `pharmacy_list.pdf`
- `physio_summary.pdf`
- `er_note.pdf`

### 2. **Upload Demo Files to Blob Storage**
Run from repo root:
```bash
python scripts/upload_demo_blobs.py
```
- This uploads PDFs to the `demo/` folder in Azure Blob
- Requires `AZURE_STORAGE_CONNECTION_STRING` to be configured in `.env`

### 3. **Test `/load_demo` from CLI**
```bash
curl -X POST https://ai-delivery-sandbox-production-d1a7.up.railway.app/load_demo \
  -H "Authorization: Bearer <your_token>"
```
Should return:
```json
{
  "session_key": "abc123...",
  "source": "family_doctor_visit.pdf",
  "source_url": "https://..."
}
```

### 4. **Run `/ask_vector` on That Session**
```bash
curl -X POST https://ai-delivery-sandbox-production-d1a7.up.railway.app/ask_vector \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"session_key": "abc123...", "query": "What medications am I taking?"}'
```
✅ Should return a GPT answer referencing that PDF content.

### 5. **Confirm in `/summary` and `/export`**
Verify structured records are available and the export includes usable output.

## ✅ Done When
- CLI test flow is verified from upload → load → ask → summary/export
- Demo files are indexed and GPT-ready
- This process can be repeated reliably for multiple test files

Let Stewart know when complete so public testers can be onboarded using this method.