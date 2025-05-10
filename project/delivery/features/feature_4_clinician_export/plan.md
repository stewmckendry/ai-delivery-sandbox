## 🧭 Feature Area 4: Clinician Export – Plan

### 🎯 Goal
Enable users to export their recovery data for clinical use, in both:
- **PDF**: A readable summary for patients, coaches, or clinicians
- **FHIR**: A structured JSON conforming to clinical data standards (Condition, Observation, CarePlan)

### 📌 Scope

- Build export_summary tool to:
  - Fetch recovery state and symptom logs
  - Format data into PDF using HTML+CSS templating (e.g. WeasyPrint)
  - Convert to FHIR JSON bundle using `epic_writer`
- Outputs returned to GPT and/or pushed to Epic sandbox
- Respect schema and validation constraints from YAMLs

#### ✅ In Scope
- PDF summary generation with Jinja2 or HTML template engine
- FHIR bundling logic for Condition, Observation, CarePlan
- Tool integration for `export_summary`
- Optional Epic sandbox push (POST stub)
- Unit tests and schema validation

#### ❌ Out of Scope
- Epic OAuth flow or real auth integration
- Full EHR bidirectional sync
- Multi-language PDF exports

### 📂 Outputs
| Phase   | Output Files |
|---------|------------------------------|
| Plan    | `plan.md`, `task_list.md` |
| Design  | `design.md`, `schema_notes.md` |
| Build   | `export_summary.py`, `epic_writer.py` |
| Deploy  | Integration test or manual FHIR push stub |
| Test    | Contract + schema validation tests |

### ✅ Alignment
- App Features: 6 (Clinician handoff), 4 (Export tools)
- Architecture: Tracker DB, YAML inputs, FastAPI, FHIR

### 🔗 Dependencies
- Uses tracker state + logs from existing DB
- FHIR format defined by HL7 spec + `epic_fhir_write_spike.md`
- PDF logic requires exportable HTML formatting

### 🧠 Assumptions
- Tracker and symptom logs are complete at export time
- YAML validation has already run
- Users request export via GPT tool with user_id context

### 📋 Task List

#### 📁 Planning
- [x] Create new task in `feature_scope_tracker.md`
- [x] Draft and commit `plan.md` and `task_list.md`

#### 📐 Design
- [x] Define PDF layout and example content
- [x] Draft FHIR JSON structure (Condition, Observation, CarePlan)
- [x] Document schema in `schema_notes.md`
- [x] Capture decisions and logic in `design.md`

#### 🛠 Build
- [ ] Build `export_summary.py` API tool (FastAPI-compliant)
- [ ] Build `epic_writer.py` to assemble FHIR bundle
- [ ] Build PDF export using Jinja2 or HTML template
- [ ] Integrate PDF + FHIR in tool response

#### 🧪 Test
- [ ] Unit test `epic_writer` with sample logs
- [ ] Validate JSON schema against FHIR
- [ ] Test PDF output layout + edge cases
- [ ] Create integration test stub (POST to Epic mock)

#### ✅ Wrap
- [ ] Confirm outputs against `delivery_guidelines.md`
- [ ] Log reasoning trace and task metadata
- [ ] Notify Human Lead for approval