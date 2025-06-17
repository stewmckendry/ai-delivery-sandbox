# 🛠️ Task 305: Refactor ETL Outputs for Cloud Deployment

## 🎯 Goal
Ensure that all ETL output files (summaries, audit logs, diagnostics) are written to persistent cloud storage instead of ephemeral local filesystem, which does not persist on Railway.

---

## 🔍 Affected Outputs
Currently written to `logs/` or project root:
- `logs/blob_runs/<session>_summary.md`
- `logs/portal_runs/<portal>_summary.md`
- `audit.json` (local JSON file)
- Any direct `Path(...).write_text()` calls in `orchestrator.py` or `etl`

---

## ✅ Refactor Targets
1. **Summaries**
   - 🔁 Replace `Path(...)/summary.md` with blob upload:
     ```python
     blob.upload_text("summaries/<session>.md", summary)
     ```
   - Optionally return the summary in the `/process` response

2. **Audit Log**
   - 🔁 Replace local JSON writes with one of:
     - Write per-session logs to blob: `audit/<session>.json`
     - Or store log events in Azure SQL with timestamp & session

3. **Other Logs or Files**
   - ✅ Confirm no other persistent file writes are made in `main.py`, `status.py`, or `rag.py`
   - ❌ Do not write `.md`, `.txt`, `.json` to the container’s `/app` folder

---

## 🧪 Testing
- Deploy to Railway and upload file via `/upload`
- Trigger `/process`, check Azure Blob for:
  - `summaries/<session>.md`
  - `audit/<session>.json` (or verify SQL log entries)
- Query `/summary` and `/ask` to validate data still usable

---

## 📦 Suggested Blob Structure
```
/summaries/<session>.md
/audit/<session>.json
/uploads/<session>/<filename>.pdf
```

---

## ✅ Done When
- No local `.write_text()` persists beyond session
- Blob or SQL used for all ETL outputs
- End-to-end flow works identically via Railway and GPT