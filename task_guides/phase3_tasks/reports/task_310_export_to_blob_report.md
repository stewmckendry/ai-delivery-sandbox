# ✅ Task 310 Report: Export to Azure Blob + Signed URL

## 🎯 Goal
Fix `/export` so it returns a signed Azure Blob URL instead of a direct file response, enabling compatibility with GPT tool calls and browser-based downloads.

---

## 🔧 Summary of Work
- ✅ Created a helper function in `blob.py` to:
  - Upload files to Azure Blob
  - Return a signed SAS URL for secure download

- ✅ Refactored `app/api/export.py` to:
  - Upload exported Markdown and PDF to Blob
  - Return `{ "status": "ok", "download_url": "..." }` JSON response

- ✅ New test: `tests/test_export_api.py` to verify URL format and behavior

---

## 🧪 Testing
- ✅ `pytest -k export_api -q` → Passed export-specific test cases
- ✅ `pytest -q` → Full suite passed
- ✅ Verified that Markdown and PDF exports result in Blob URLs
- ✅ Export tool now works in GPT and browser contexts

---

## 📁 Updated Files
- `app/api/export.py`
- `app/storage/blob.py`
- `tests/test_export_api.py` (new)

---

## ✅ Outcome
- Export feature is now fully GPT-compatible
- PDF and Markdown exports are downloadable via time-limited Blob URL
- This makes it safe and scalable for both chat-based and browser workflows