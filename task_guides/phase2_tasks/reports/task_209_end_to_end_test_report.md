# ✅ Task 209 Report: End-to-End Test (Operator Upload → RAG)

## 🧪 Goal
Validate that users can upload HTML/PDF files collected via Operator and retrieve structured records via the full toolchain: `/process`, `/ask`, `/export`, and `/summary`.

---

## 🔄 Test Flow + Results

### 1. File Collection
- ✅ Operator used to log in to Strava and save activity data as `.html`
- ✅ File renamed and inspected locally

### 2. Upload
- ✅ `upload_to_blob.py` successfully uploaded file using SAS
- ✅ Metadata confirmed in `audit.json`

### 3. ETL (/process)
- ✅ FastAPI started via new `main.py`
- ✅ POST to `/process` succeeded
- ✅ Blob downloaded, parsed, inserted 12 structured records
- ✅ Summary saved to `logs/blob_runs/test_user_summary.md`
- ⚠️ Required SQL table reset due to schema mismatch

### 4. Ask Tool
```bash
python scripts/ask_tool.py --query "What are my latest test results?"
```
- ✅ Answered using lab results
```bash
python scripts/ask_tool.py --query "What activity did I do?"
```
- ✅ Answered using Strava HTML content

### 5. Export Tool
```bash
python scripts/export_records.py --format markdown --output out.md
```
- ✅ Markdown output matched expected labs, visits, activities

### 6. Status (/summary)
```bash
curl "http://localhost:8000/summary?session_key=test_user" | jq
```
- ✅ Uploads and processing timestamps confirmed
- ⚠️ Multiple uploads for same file present (no deduplication)

---

## 🧱 Challenges + Fixes
| Challenge | Fix |
|----------|-----|
| Azure SDK import | Installed `azure-storage-blob` only (not `azure`) |
| SAS token missing resource types | Regenerated with `Container` + `Object` access |
| Filename with spaces | Quoted path or renamed locally |
| HTTP 400 on upload | Added `x-ms-blob-type: BlockBlob` header |
| Missing connection string | Added to `.env` as `AZURE_STORAGE_CONNECTION_STRING` |
| SQL column mismatch | Dropped and recreated `structured_records` table |
| Route conflict on `/status` | Moved full summary to `/summary` route |

---

## ✅ Outcome
All major steps in the user flow validated:
- Operator-captured data → Upload → ETL → Ask/Export/Status
- Data was accurately parsed and structured
- Tools from Phase 1 remain functional and reliable

This confirms the MVP is working E2E and ready for multi-user scaling and polish.