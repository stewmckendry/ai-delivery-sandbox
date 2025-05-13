# 🧠 Concussion Recovery App – Data Flow Master (v2)

This is the updated, end-to-end source of truth for how data flows from GPT intake to SQL export and dashboard reporting.

---

## 1. 🌟 User Journey Overview

| Step | Tool | Description |
|------|------|-------------|
| 1 | `get_triage_flow`, `get_triage_question` | Load YAML-driven triage Q&A |
| 2 | `log_incident_detail` | Log responses to `TriageResponse`, plus metadata to `IncidentReport` |
| 3 | `assess_concussion` | Evaluate red flag symptoms → `ConcussionAssessment` |
| 4 | `log_symptoms` | Periodic symptom check-in → `SymptomLog` |
| 5 | `get_stage_guidance` | Infer recovery stage → `StageLog` or `RecoveryCheck` |
| 6 | `export_summary` | Export PDF + FHIR care handoff summary |
| 7 | `export_to_sql` | Export all tables for Power BI |

---

## 2. 🧩 Schema Map (Models + Tables)

| Model | Table | Purpose |
|-------|-------|---------|
| TriageResponse | triage_response_export | One row per Q&A |
| IncidentReport | incident_report_export | One row per triage session |
| SymptomLog | symptom_log_export | Follow-up symptom check-ins |
| ConcussionAssessment | concussion_assessment_export | Red flag summary |
| StageLog | stage_result_export | Inferred recovery stage from triage/check-ins |
| RecoveryCheck | recovery_check_export | One-off stage inference from quick chat |

---

## 3. 🔧 Tool Coverage

- `log_incident_detail.py` → logs to TriageResponse + IncidentReport
- `symptom_logger.py` → logs symptoms with validation
- `assess_concussion.py` → logs red flag outcome
- `get_stage_guidance.py` → logs to StageLog or RecoveryCheck
- `export_summary.py` → writes PDF + FHIR output
- `export_to_sql.py` → exports all models
- `get_symptom_log_map.py` → serves follow-up schema
- `get_linked_symptoms.py` → retrieves last-known symptoms

---

## 4. 🧪 Validation Logic

- `symptom_library.py` ensures all symptom IDs match YAML
- `validator.py` can audit schema drift across SymptomLog entries

---

## 5. 📦 YAML Schemas

| File | Purpose |
|------|---------|
| `triage_map.yaml` | Initial Q&A flow and symptom triggers |
| `symptom_log_map.yaml` | Follow-up check-in structure |
| `symptoms_*.yaml` | Source of truth for valid symptom IDs and tags |

---

## 6. 📄 Power BI Reporting Strategy

- Joinable tables via `user_id` and timestamp proximity
- Cohort-safe aggregation (no raw `user_id` exposure)
- Flags for red symptoms, recovery progression, and symptom frequency

---

## 7. 🪤 Gaps Resolved in v2

- Removed legacy `TrackerMetadata`
- Unified YAML + model validation
- Structured follow-up logging with SymptomLog
- Added RecoveryCheck model for stage logic outside of triage
- Export tools cover all models