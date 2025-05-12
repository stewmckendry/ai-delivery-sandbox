# ✅ Task List – Implement Data Flow Audit

This list tracks the delivery of fixes and enhancements from the data flow master audit.

---

## 🔧 1. Schema + Model Updates

### [x] Add `TriageResponse` model
### [x] Add optional `IncidentReport` model
### [ ] Rename `metadata` field → `log_metadata`
### [ ] Add missing context fields to `SymptomLog`
### [ ] Add `StageLog` and `ConcussionAssessment` to model list

---

## 🛠️ 2. Tool Updates

### [x] Update `log_incident_detail.py`
### [x] Update `export_to_sql.py`
### [x] Extend `assess_concussion.py`
### [x] Extend `get_stage_guidance.py`
### [ ] Update `symptom_logger.py`, `db_writer.py` to use new SymptomLog fields
### [ ] Refactor YAML parsing into `symptom_library.py`

---

## 🧪 3. Validation + Schema Alignment

### [ ] Introduce `symptom_log_map.yaml` for follow-ups
### [ ] Add YAML-to-schema audit in `validator.py`

---

## 🧼 4. Cleanup

### [ ] Remove unused `TrackerMetadata` refs
### [ ] Replace old doc `data_flow_addendum.md`
### [ ] Fix export_to_sql to align with `SymptomLog`

---

## 📍 Tracking

- All deliverables to be committed to: `sandbox-silver-tiger`
- Tag completed steps in commit messages: `#data-flow-fix`, `#triage-db`, etc.