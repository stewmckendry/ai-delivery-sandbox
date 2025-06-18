# 📤 Task 310: Export to Azure Blob + Return Signed URL

## 🎯 Goal
Fix the `/export` endpoint so that it returns a **time-limited Azure Blob URL** instead of a raw file response. This avoids issues with Custom GPT tool calls that can't handle direct file responses.

---

## 🔍 Current Behavior
- `GET /export` returns the record set as:
  - JSON
  - Markdown
  - PDF (via `FileResponse`)
- This works in browser, but fails in GPT or plugin context because file streams aren’t supported

---

## ✅ New Behavior
- Convert export results to bytes or text
- Upload to Azure Blob in a path like:
  - `exports/<session_key>_<timestamp>.pdf` (or `.md` / `.json`)
- Return a signed SAS URL that expires after 15–60 minutes
- Update the endpoint to return:
```json
{
  "status": "ok",
  "download_url": "https://..."
}
```

---

## 📦 Files to Update
- `app/api/export.py`
- `app/storage/blob.py` (add helper like `upload_file_and_get_url()`)

---

## ✅ Done When
- GPT tool calls to `/export` succeed with PDF/Markdown/JSON format
- Blob object is time-limited and session-scoped
- URL is returned as JSON for easy embedding

---

## 🔐 Bonus Consideration
- Ensure filename includes session or hash to avoid collision
- Consider optional query like `?inline=false` if download preferred