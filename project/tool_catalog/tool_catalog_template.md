# 🔧 Tool Catalog Template – Best Practice

## 📌 Overview
Describe what the tool catalog covers and how tools are registered, tagged, and discovered.

- **Purpose:** Maps FastAPI tools available to GPTs or frontend clients
- **Integration Format:** OpenAPI, manually tagged, or YAML

## 📘 Tool Registry
| Tool Path           | Function Summary                          | Input Schema        | Output Schema       | Tags             |
|---------------------|--------------------------------------------|---------------------|----------------------|------------------|
| `/log_incident_detail` | Capture triage Q&A                      | IncidentInput       | SuccessResponse      | `triage`, `log`  |
| `/assess_concussion`   | Flag red flags from YAML config        | SymptomSet          | FlagResponse         | `concussion`     |
| `/symptom_logger`      | Store symptom log + metadata           | SymptomLogInput     | SuccessResponse      | `symptom`, `log` |
| `/get_stage_guidance`  | Infer recovery stage                   | TrackerState        | StageOutput          | `stage`, `inference` |
| `/export_summary`      | Generate PDF + FHIR + URL              | user_id             | ExportBundle         | `export`, `report` |

## 🧪 Testing Tools
- How tools are stubbed or mocked for test
- Unit vs end-to-end test strategies

## 🔐 Auth + Access Rules
- Which tools are public vs gated?
- Rate limiting, traceability, and logging

## 🏷️ Tag Taxonomy
- Use tags like: `triage`, `log`, `report`, `QA-only`, `internal`, `yaml-driven`

---
Include links to OpenAPI file, validator schemas, test coverage reports if available.