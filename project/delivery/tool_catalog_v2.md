# 🛠️ Tool Catalog (v2) – Concussion Recovery App

This document catalogs all tools implemented as FastAPI routes used by the Custom GPT or frontend.

---

## 1. Intake + Triage

| Route | Description |
|-------|-------------|
| `/get_triage_flow` | Returns full triage map (from YAML) |
| `/get_triage_question` | Returns a specific triage question block |
| `/log_incident_detail` | Logs user Q&A to `TriageResponse` + structured metadata to `IncidentReport` |

---

## 2. Symptom Logging + Assessments

| Route | Description |
|-------|-------------|
| `/log_symptoms` | Logs structured symptom check-in to `SymptomLog` |
| `/get_symptom_log_map` | Returns follow-up symptom schema YAML (parsed) |
| `/get_linked_symptoms/{user_id}` | Retrieves previously reported symptoms for user |

---

## 3. Assessment Engines

| Route | Description |
|-------|-------------|
| `/assess_concussion` | Evaluates red flags and returns `ConcussionAssessment` |
| `/get_stage_guidance` | Infers recovery stage → logs to `StageLog` |

---

## 4. Export + Reporting

| Route | Description |
|-------|-------------|
| `/export_summary` | Generates and stores clinical PDF export |
| `/export_to_sql` | Pushes all tables to Azure SQL (Power BI sync) |

---

## 5. Internal + Validation

| Route | Description |
|-------|-------------|
| n/a (CLI only) | `validator.py` can audit schema vs YAML definitions |

---

## 6. Tool Coverage Map

| Tool File | Routes Defined |
|-----------|----------------|
| `log_incident_detail.py` | `/log_incident_detail` |
| `symptom_logger.py` | `/log_symptoms` |
| `get_triage_flow.py` | `/get_triage_flow` |
| `get_triage_question.py` | `/get_triage_question` |
| `get_symptom_log_map.py` | `/get_symptom_log_map` |
| `get_linked_symptoms.py` | `/get_linked_symptoms/{user_id}` |
| `assess_concussion.py` | `/assess_concussion` |
| `get_stage_guidance.py` | `/get_stage_guidance` |
| `export_summary.py` | `/export_summary` |
| `export_to_sql.py` | `/export_to_sql` |

---

## 🔄 Next
- Consider OpenAPI sync with `openapi.json`
- Extend tools with usage examples for testing and QA