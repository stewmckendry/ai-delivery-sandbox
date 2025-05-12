# ✅ Task List – Implement Data Flow Audit

This list tracks the delivery of fixes and enhancements from the data flow master audit.

---

## 🔧 1. Schema + Model Updates

### [x] Add `TriageResponse` model
- Fields: `user_id`, `question_id`, `question_text`, `answer`, `timestamp`
- Table: `triage_response_export`
- File: `db_models.py`

### [x] Add optional `IncidentReport` model
- Fields: all structured metadata from triage_map.yaml
- File: `db_models.py`

### [ ] Rename `metadata` field → `log_metadata`
- File: `SymptomLog` in `db_models.py`
- Update all uses in `symptom_logger`, `db_writer`, etc.

---

## 🛠️ 2. Tool Updates

### [x] Update `log_incident_detail.py`
- Log each Q&A from triage into `TriageResponse`
- Optionally create single-row `IncidentReport`

### [x] Update `export_to_sql.py`
- Include new model/table if created

### [ ] Extend `assess_concussion.py`
- Optionally log red flag assessment result to DB

### [ ] Extend `get_stage_guidance.py`
- Optionally log inferred stage to DB

---

## 🧪 3. Validation + Reporting

### [ ] Audit YAML vs model field sync
- Files: `triage_map.yaml`, `symptoms_*.yaml`, `models/`, `db_models.py`

### [ ] Update Power BI SQL views
- Reflect new triage and stage data
- Ensure aggregation, anonymity

---

## 🧼 4. Cleanup

### [ ] Remove unused `TrackerMetadata` refs
- Files: `log_incident_detail.py`, legacy code

### [ ] Replace old doc `data_flow_addendum.md`
- New source: `data_flow_master.md`

### [ ] Fix export_to_sql to align with SymptomLog and canonical schema
- Refactor symptom_log_export logic
- Reference: data_flow_master.md

---

## 📍 Tracking

- All deliverables to be committed to: `sandbox-silver-tiger`
- Tag completed steps in commit messages: `#data-flow-fix`, `#triage-db`, etc.