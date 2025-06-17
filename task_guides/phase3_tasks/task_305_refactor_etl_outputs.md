# 🛠️ Task 305: Refactor ETL Outputs for Privacy-Safe Cloud Deployment

## 🎯 Goal
Ensure ETL outputs avoid persistent storage of any sensitive health data. Refactor current file writes to comply with privacy-first design in the Railway cloud environment.

---

## 🔍 Outputs to Address
### Remove Persistent Writes for:
- `logs/blob_runs/<session>_summary.md`
- `logs/portal_runs/<portal>_summary.md`
- Direct `.write_text()` of ETL summaries or parsed content

### Allow Minimal Metadata:
- Audit log of filename, portal, timestamp only
- Already uploaded files (PDF/HTML) can remain in Azure Blob with short expiration (24–72 hrs)

---

## ✅ Refactor Instructions

### 1. **ETL Summaries**
- ❌ Do not write summaries to disk or blob
- ✅ Return summary as part of the `/process` API response (inline only)
- ✅ Redact sensitive content if needed (configurable)

### 2. **Audit Logging**
- ✅ Keep metadata like:
  ```json
  {
    "session_key": "abc123",
    "filename": "lab_2024-01-01.pdf",
    "portal": "lifelabs",
    "timestamp": "2025-06-17T10:00:00Z"
  }
  ```
- ✅ Store in Azure SQL or blob as `audit/<session>.json`
- ❌ Do not include text or record content

### 3. **Uploaded Files**
- ✅ Stored in Azure Blob with SAS
- ✅ Ensure `upload.py` confirms files expire in < 72 hours
- ✅ OK to process and discard in memory

---

## 📦 Updated Blob Structure
```
/audit/<session>.json
/uploads/<session>/<filename>.pdf
```

No longer write:
```
/logs/
/summaries/
```

---

## ✅ Done When
- No PHI is stored outside runtime memory or expiring blob
- ETL summaries are inline only
- Audit log contains only minimal metadata
- End-to-end testing confirms `/process` works without persistent writes