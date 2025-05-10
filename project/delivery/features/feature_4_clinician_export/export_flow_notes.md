## 🧾 Export Flow Addendum: PDF + FHIR

This note explains how recovery data is extracted, formatted, and returned via the `export_summary` tool.

---

### 🛠️ Tool Entrypoint: `export_summary`
File: [`app/tools/export_summary.py`](../../../../app/tools/export_summary.py)
- Triggered by GPT or frontend tool
- Input: `user_id`
- Output: `ExportResponse` with:
  - `pdf_url`: Link to summary PDF
  - `fhir_bundle`: JSON with Condition, Observations, CarePlan

### 📄 PDF Generation
**Function**: `render_pdf(...)`
File: [`app/engines/pdf_renderer.py`](../../../../app/engines/pdf_renderer.py)
- Loads `clinical_summary.html` from GitHub
- Renders using Jinja2 with user data
- Converts to PDF using WeasyPrint
- Outputs local temp file path

### 📦 FHIR Generation
**Function**: `build_fhir_bundle(...)`
File: [`app/engines/epic_writer.py`](../../../../app/engines/epic_writer.py)
- Takes tracker + symptoms as input
- Returns HL7-compliant FHIR `Bundle` with:
  - `Condition`: SNOMED-coded concussion
  - `Observation[]`: One per symptom
  - `CarePlan`: Summary guidance + inferred time window

### ☁️ Upload Handling
**Function**: `upload_to_storage(...)`
File: `export_summary.py`
- Currently stubbed — returns simulated public URL
- Will be replaced with cloud upload (Azure Blob, S3, etc.)

---

### 🧩 Notes
- All tools are modular: DB fetch → PDF → FHIR → Upload
- PDF and JSON both returned in a single tool response
- This design avoids large GPT payloads and supports export traceability

✅ Future step: swap storage stub for secure cloud storage
✅ Test coverage in `test_export_summary.py`