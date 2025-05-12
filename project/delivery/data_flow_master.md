# 🧠 Concussion Recovery App – End-to-End Data Flow Audit (Source of Truth)

This document captures the full pipeline of data flow in the Concussion Recovery App, from user interaction to data persistence and export. It includes structured models, tool mappings, database tables, user flows, and reporting expectations. It also identifies implementation gaps and proposes corrective actions.

---

## 🧭 1. User Journey Overview

### Step-by-Step Sequence
1. **Start Triage**
   - Tool: `get_triage_flow`, `get_triage_question`
   - Source: `reference/triage_map.yaml`
2. **Complete Triage Q&A**
   - Tool: `log_incident_detail`
   - New Model Recommended: `TriageResponse`
3. **Assess Red Flags**
   - Tool: `assess_concussion`
   - Source: `reference/symptoms_red_flag.yaml`
4. **Log Symptoms**
   - Tool: `symptom_logger.py`
   - Model: `SymptomLog` (in `app/models/symptoms.py`)
5. **Infer Recovery Stage**
   - Tool: `get_stage_guidance`
   - Engine: `stage_engine.py`
6. **Export to Dashboard**
   - Tool: `export_to_sql`
   - Writer: `db_writer.py`

Note: If a user begins at step 4 or 5, system will continue to function but some metadata context may be missing.

---

## 🧬 2. Data Model Mapping (by Stage)

### Triage Questions and Metadata
- Source: `reference/triage_map.yaml`
- Captured fields:
  - `reporter_role`, `sport_type`, `age_group`, `team_id`, `injury_date`, `injury_context`, `symptoms`, `lost_consciousness`, `seen_provider`, `diagnosed_concussion`, `still_symptomatic`, `cleared_to_play`
- These should be explicitly defined in a new model (see below)

### Symptom Logging
- Source: `symptoms_*.yaml`
- Model: `SymptomLog`
- Enhancement: Rename reserved `metadata` field to `log_metadata`

### Stage Inference
- Engine: `stage_engine.py`
- Output not currently stored in DB; should optionally be logged

### Export to SQL
- Tool: `export_to_sql.py`
- Table: `symptom_log_export`

---

## 🧾 3. Model Summary (Revised)

| Model Name | Purpose | Attributes | Usage Points | Tool References | File | Status | Recommendation |
|------------|---------|------------|--------------|------------------|------|--------|----------------|
| SymptomLog | Stores symptom logs and metadata | `user_id`, `timestamp`, `symptoms`, `log_metadata`, `incident_context`, ... | Logging and export | `symptom_logger`, `export_to_sql` | `models/symptoms.py`, `db_models.py` | ✅ Active | Rename `metadata` field |
| TriageResponse | Store each triage Q&A | `user_id`, `question_id`, `question_text`, `answer`, `timestamp` | `log_incident_detail.py` | proposed | new | 🔧 Needed | Implement as new model/table |
| IncidentReport | Optional: store one row per triage session | `user_id`, structured triage fields | `log_incident_detail.py`, export | new | proposed | 🔧 Needed | Recommended for export clarity |

---

## 🗄️ 4. Database Tables Overview

| Table | Purpose | Fields | Tools | Model | File | Status | Recommendation |
|--------|---------|--------|-------|--------|------|--------|----------------|
| symptom_log_export | Store symptoms + context | `user_id`, `timestamp`, `symptoms`, `log_metadata`, etc. | logger/export | `SymptomLog` | `db_models.py` | ✅ Exists | Clean + normalize fields |
| triage_response_export | New table to store Q&A | `user_id`, `question_id`, `answer`, `timestamp` | triage logger | `TriageResponse` | new | 🔧 Needed | Create for auditability |
| YAML (triage_map.yaml) | Source of truth for triage logic | n/a | triage engine/tools | n/a | ✅ Source | Ensure synced with models |

---

## 📊 5. Power BI Reporting Plan

Reports should be **aggregate and anonymized**:
- Symptom trends by age group, team, or sport
- Red flag frequency rates
- % cleared to play vs not
- % who saw provider or were diagnosed
- Stage recovery progression
- Triage completion vs skipped rates

### Safeguards:
- No raw `user_id` exposed
- Group counts <5 suppressed
- Views use demographics + cohorts only

---

## ⚠️ 6. Gaps and Proposed Fixes

| Area | Issue | Fix |
|------|-------|-----|
| Triage fields | YAML-only, not stored | Create `TriageResponse` model/table |
| metadata | Reserved keyword in SQLAlchemy | Rename to `log_metadata` |
| Red flag | Not stored | Add to `SymptomLog` or `IncidentReport` |
| Stage inference | Not stored | Optional log output to DB |
| YAML-to-model drift | Untracked | Audit YAML vs schema |

---

## ✅ 7. What’s Implemented vs Missing

### Implemented
- All triage logic
- Symptom logging + export

### Missing / Partial
- Triage responses
- Field-level metadata
- Red flag logging
- Stage persistence

---

## 📘 8. Next Steps
- [ ] Implement `TriageResponse` model and table
- [ ] Extend `log_incident_detail.py` to write triage answers to DB
- [ ] Rename reserved `metadata` field → `log_metadata`
- [ ] Optionally log output of `assess_concussion` and `get_stage_guidance`
- [ ] Update Power BI view definitions
- [ ] Replace `data_flow_addendum.md` with this document

---

## 🧩 SYMPTOM LOGGING ADDENDUM

### Why This Matters
- Symptom check-ins are a central part of tracking concussion recovery.
- Structured YAML defines symptoms used in triage and assessment tools.
- Current logging is inconsistent, under-specified, and missing metadata fields.

### Current Issues
- `SymptomLog` uses reserved field `metadata`.
- Fields like `reporter_role`, `incident_context`, etc., only captured during triage.
- No structured schema like `triage_map.yaml` exists for symptom check-ins.
- Validation against `symptoms_*.yaml` is ad hoc, lacks audit trail.

### Fix Plan
1. **Model Updates**
   - Rename `metadata` → `log_metadata` in `SymptomLog`
   - Add missing fields: `incident_context`, `reporter_role`, etc.

2. **Schema and Validation**
   - Introduce `symptom_log_map.yaml` as structured follow-up schema
   - Add validation script comparing model vs YAML field alignment

3. **Codebase Refactor**
   - Move all YAML parsing to `symptom_library.py`
   - Use `SymptomDefinition` type to unify structure across tools

4. **Downstream Use**
   - Use shared definitions in `export_to_sql`, `pdf_renderer`, `epic_writer`
   - Power BI exports should pull both `symptoms` and `log_metadata`

5. **Join Strategy**
   - `SymptomLog` joins to `IncidentReport` via `user_id` + timestamp proximity
   - Minimal intentional overlap — scope is different (incident vs check-in)