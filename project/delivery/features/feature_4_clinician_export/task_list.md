## ✅ Task List – Feature 4: Clinician Export

### 📁 Planning
- [x] Create new task in `feature_scope_tracker.md`
- [x] Draft and commit `plan.md` and `task_list.md`

### 📐 Design
- [ ] Define PDF layout and example content
- [ ] Draft FHIR JSON structure (Condition, Observation, CarePlan)
- [ ] Document schema in `schema_notes.md`
- [ ] Capture decisions and logic in `design.md`

### 🛠 Build
- [ ] Build `export_summary.py` API tool (FastAPI-compliant)
- [ ] Build `epic_writer.py` to assemble FHIR bundle
- [ ] Build PDF export using Jinja2 or HTML template
- [ ] Integrate PDF + FHIR in tool response

### 🧪 Test
- [ ] Unit test `epic_writer` with sample logs
- [ ] Validate JSON schema against FHIR
- [ ] Test PDF output layout + edge cases
- [ ] Create integration test stub (POST to Epic mock)

### ✅ Wrap
- [ ] Confirm outputs against `delivery_guidelines.md`
- [ ] Log reasoning trace and task metadata
- [ ] Notify Human Lead for approval