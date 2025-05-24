## WP20 Implementation Notes – Google Drive Integration

### 🧩 Scope Recap
WP20 added support for exporting and retrieving final artifacts to/from Google Drive. These tools enable structured, versioned document storage tied to gate workflows in PolicyGPT.

### ✅ Tools Delivered
- `storeToDrive.py` – uploads PDF version of final artifact to structured Drive folder path
- `fetchFromDrive.py` – retrieves uploaded PDF based on artifact metadata
- Markdown-to-PDF rendering built using `weasyprint`

---

### 🛠️ Key Design Decisions

#### 📄 Document Format
- Output format: **PDF** (for formatting, interoperability, and downstream usage)
- Markdown is rendered and styled into styled PDFs

#### 📂 Folder Structure
- Upload path: `PolicyGPT/gate_<gate_id>/<artifact_id>/<filename>`
- Filename format: `<artifact_id>_v<version>_<timestamp>.pdf`
- Timestamp avoids overwrites and enables version tracking

#### 🔒 OAuth + Auth
- Drive access via Google service account
- Auth key path defined via `.env` or Railway cloud env vars
- Permission managed by sharing root PolicyGPT folder with the service account

---

### 🔗 Toolchain Integration
- `storeToDrive.py` is now invoked in `assemble_artifact_chain.py` as the final commit step
- `DocumentVersionLog` DB updated:
  - `google_doc_url`: Drive preview link
  - `file_path`: PDF filename

---

### 🧪 Testing
- Manual and automated tests confirm upload + fetch
- Live artifacts are successfully stored + retrievable
- Test files + logs committed under `project/test/WP20/`

---

### ⚠️ Known Issues
- Table of contents links show anchor warnings in `weasyprint`
- Only PDF is supported (no markdown preview or docx editable format yet)

---

### 🔭 Future Enhancements
- Add support for preview fetch or docx export
- Handle project ID (currently missing from folder schema)
- Optimize schema validation across tools

---

📁 This document summarizes the architectural and implementation work completed in WP20.
