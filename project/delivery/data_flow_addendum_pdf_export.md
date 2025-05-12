# 📎 Data Flow Addendum – PDF & FHIR Export Update

This document supplements `data_flow_master_v2.md` with recent fixes to the PDF and FHIR export logic to align with the structured schema.

---

## 🧾 Purpose
Ensure that summary exports reflect the structured `SymptomLog`, `IncidentReport`, and `StageLog` models introduced in the schema overhaul.

---

## 🔧 Components Updated

| File | Description |
|------|-------------|
| `db_reader.py` | Implements `get_export_bundle()` to load symptoms, stage, and incident context |
| `pdf_renderer.py` | Dynamically renders user ID, recent symptoms, reporter role, and inferred stage |
| `epic_writer.py` | Emits FHIR Observation entries for each symptom with metadata |
| `export_summary.py` | Orchestrates the export by calling all engines |

---

## 🧱 Data Sources
- `SymptomLog.symptoms` (parsed per symptom)
- `SymptomLog` context metadata (`reporter_type`, `sport_type`, etc.)
- `StageLog.inferred_stage`
- `IncidentReport` fallback where available

---

## 📄 PDF Output
Includes:
- User ID
- Inferred stage
- 5 most recent symptoms with severity and context
- Timestamped export info

---

## 💊 FHIR Bundle Output
- One Observation per symptom log item
- Encodes metadata as `extension` blocks
- Additional Observation for inferred stage

---

## 🔄 Notes
- `get_export_bundle()` replaces nonexistent `get_tracker_and_logs()`
- Schema now supports richer export and auditability

This update closes gaps flagged during the final QA prep round and aligns export tools with the new structured data flow.