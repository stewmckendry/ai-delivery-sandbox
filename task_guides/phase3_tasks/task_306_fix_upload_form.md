# 🛠️ Task 306: Fix Upload Form for Web UI

## 🎯 Goal
Fix the `/upload` web interface to ensure Azure uploads work reliably and give the user visual feedback.

---

## 🧩 Bugs to Fix

### 1. **Azure Upload Fails (400)**
- ❌ `PUT` to Azure Blob SAS URL fails with:
  - `400 Bad Request: An HTTP header that's mandatory for this request is not specified.`
- 🔍 Cause: Missing `x-ms-blob-type: BlockBlob` header in JavaScript upload
- ✅ Fix:
```js
fetch(data.url, {
  method: 'PUT',
  body: file,
  headers: { 'x-ms-blob-type': 'BlockBlob' }
})
```

### 2. **No File Display After Selection**
- ❌ After choosing a file with `<input type="file">`, no filenames are shown
- ✅ Fix: Add a UI element (list or `<ul>`) that appends each selected file with name and status

### 3. **No Feedback for Drag & Drop Files**
- ❌ Dragged files are not shown to the user until upload is attempted
- ✅ Fix: Reuse same file-listing mechanism from step 2 for drag events

---

## ✅ Done When
- Upload via file picker or drag-and-drop works with Azure Blob
- Uploaded files are listed with a status message (e.g., "Uploading...", "Uploaded ✔")
- Failures show error clearly (e.g., "Upload failed: 400")

---

## 📁 Files to Update
- `app/web/upload_form.html` (JavaScript + DOM update)
- ✅ No changes needed on backend routes unless error persists

---

Let Stewart know when fixed so he can re-test via:  
`https://ai-delivery-sandbox-production-d1a7.up.railway.app/upload?session=test_user&portal=lifelabs`