# 🔄 Data Flow Template – Best Practice

## 🧭 Overview
Describe what the flow is, the entities it touches, and the scope (e.g. triage to export).

## 📉 High-Level Diagram
```
[User Input] → [Tool Call] → [Engine Logic] → [Model Log] → [Export/Report]
```

## 📘 Step-by-Step Breakdown
| Step | Tool / Engine            | Input Source        | Output Destination     | Model(s) Affected         |
|------|--------------------------|---------------------|-------------------------|----------------------------|
| 1    | `get_triage_flow`        | triage_map.yaml     | GPT prompt             | –                          |
| 2    | `log_incident_detail`    | GPT answers         | triage_response_export | TriageResponse             |
| 3    | `assess_concussion`      | red flag YAML       | log or model           | ConcussionAssessment       |
| 4    | `symptom_logger`         | symptom_log_map     | symptom_log_export     | SymptomLog                 |
| 5    | `get_stage_guidance`     | model state         | stage inference        | StageLog (optional)        |
| 6    | `export_to_sql`          | DB models           | SQL views              | All above                  |

## 🔄 Sync / Export Processes
- How is the data exported (to SQL, PDF, FHIR)?
- Are any joins or flattening applied?

## ⚠️ Known Gaps
- What parts of the flow are not implemented or missing traceability?

---
Include sample data, YAML references, and export artifacts if available.