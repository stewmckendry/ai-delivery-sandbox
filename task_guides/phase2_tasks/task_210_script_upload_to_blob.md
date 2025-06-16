# Task 210: Script to Upload Files to Azure Blob

## 🎯 Goal
Automate file uploads to Azure Blob for repeatable test runs, enabling CLI-driven end-to-end testing of Operator-extracted files.

---

## 📋 Instructions
- Add a script `scripts/upload_to_blob.py`
- Inputs:
  - `--session-key` (e.g., test_user)
  - `--file` (local file path to upload)
  - `--portal` (optional: to store in metadata)
- Use existing `blob.generate_upload_url()`
- Upload via HTTP PUT
- Log metadata using `blob.record_upload()`

---

## 🧪 Example Usage
```bash
python scripts/upload_to_blob.py --session-key test_user --file strava.html --portal strava
```

## ✅ What to Report Back
- Output from successful upload
- Path to blob stored
- Confirmation from `/status` or `audit.json`

---

## 📂 Target Files
- `scripts/upload_to_blob.py` (new)
- Uses `app/storage/blob.py`

This enables automation of the upload step for test loops or batch file processing.