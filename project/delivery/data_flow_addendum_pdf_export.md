# 📎 Data Flow Addendum – PDF & FHIR Export Update

This document supplements `data_flow_master_v2.md` with recent fixes and enrichments to the PDF and FHIR export logic, ensuring alignment with the structured schema.

---

## 🧾 Purpose
Ensure that export outputs include:
- Structured logs from `SymptomLog`, `IncidentReport`, and `StageLog`
- Enriched context: concussion flags, extra notes, injury metadata
- Auditability and human-readable summaries

---

## 🔧 Components Updated

| File | Description |
|------|-------------|
| `db_reader.py` | Implements `get_export_bundle()` to load all structured data for a user |
| `pdf_renderer.py` | Renders injury context, flags, stage, and recent symptoms with metadata |
| `epic_writer.py` | Emits Observations for symptoms, metadata, and assessment results |
| `export_summary.py` | Gathers and uploads outputs to Azure Blob, returns signed URL and FHIR |

---

## 📄 PDF Output Enrichment

Includes:
- User ID and export time
- Injury date, reporter role, sport, age group, incident context
- Flags: `cleared_to_play`, `lost_consciousness`, `diagnosed_concussion`, etc.
- Latest stage and 5 recent symptoms with severity and extra notes

PDF uploaded to Azure Blob via `upload_to_storage()`.

---

## 💊 FHIR Bundle Enrichment

Each symptom encoded as `Observation`:
- `symptom_id`, `severity`, `timestamp`
- Context: `reporter_type`, `incident_context`, `sport_type`, `age_group`, `team_id`
- Notes: `extra_notes`

Additional Observations for:
- `Inferred Recovery Stage`
- `Concussion Assessment Summary`, `Red Flags Present`, `Concussion Likely`

---

## ✅ Outcome
Export logic is now:
- Fully aligned with structured schema
- Rich in clinical context and metadata
- Ready for use by clinicians and external dashboards

This final step ensures that insights from the recovery tracker are portable and audit-ready.