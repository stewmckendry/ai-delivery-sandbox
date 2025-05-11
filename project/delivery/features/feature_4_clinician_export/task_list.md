## ✅ Feature 4 – Task List: Clinician Export (PDF + FHIR)

### 📁 Planning
- [x] Create new task in `feature_scope_tracker.md`
- [x] Draft and commit `plan.md` and `task_list.md`

### 📐 Design
- [x] Define PDF layout and example content (`design.md`)
- [x] Draft FHIR JSON structure (Condition, Observation, CarePlan)
- [x] Document schema in `schema_notes.md`
- [x] Capture decisions and logic in `design.md`
- [x] Create `export_flow_notes.md` for tool + output explanation

### 🛠 Build
- [x] Build `export_summary.py` API tool (FastAPI-compliant)
- [x] Build `epic_writer.py` to assemble FHIR bundle
- [x] Build `pdf_renderer.py` to generate PDF
- [x] Create and commit `clinical_summary.html` template
- [x] Stub `upload_to_storage()` for simulated upload
- [x] Implement real Azure Blob upload in `upload_to_storage()`

### 🧪 Test
- [x] Unit test `epic_writer` with sample logs (`test_fhir_schema.py`)
- [x] Validate FHIR JSON bundle fields
- [x] Test PDF output rendering and file check (`test_pdf_renderer.py`)
- [x] Integration test `test_export_summary.py` for tool output

### ✅ Wrap
- [x] Confirm outputs against `delivery_guidelines.md`
- [x] Log reasoning trace and task metadata
- [x] Notify Human Lead for approval
- [x] Add Azure delivery notes (`azure_upload_notes.md`)

---

Feature complete and ready to close. Next task: prepare Feature 5 kickoff scope or delivery retrospective.