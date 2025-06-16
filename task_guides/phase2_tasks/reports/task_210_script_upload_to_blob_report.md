# ✅ Task 210 Report: Script to Upload Files to Azure Blob

## 📄 Summary
Implements a CLI script to upload Operator-generated files to Azure Blob using a SAS URL. Enables automation of the upload step for local testing or CI workflows.

## 🔧 Implementation
- `upload_to_blob.py` script:
  - Accepts `--session-key`, `--file`, `--portal`
  - Uploads via `httpx.put()` to SAS URL
  - Logs metadata with `record_upload()`
- `test_upload_to_blob.py` verifies:
  - SAS URL generation
  - File sent via HTTP PUT
  - Metadata recorded correctly

## 🧪 Testing
- ✅ `pytest -q` passed
- ✅ Simulated test verifies:
  - SAS URL used correctly
  - Upload succeeded
  - Log written with session, portal, and filename

## ✅ Files Changed
- `scripts/upload_to_blob.py`
- `tests/test_upload_to_blob.py`

## 🏁 Outcome
Uploads can now be scripted and repeated without UI. Uploads feed directly into ETL flow once `/process` is called.