# 📎 Data Flow Addendum – PDF & FHIR Export Update

This document supplements `data_flow_master_v2.md` with fixes and enrichments to the PDF and FHIR export logic, ensuring alignment with the structured schema.

---

## 🧾 Purpose
Ensure export outputs reflect all structured logs, context metadata, and recovery status.

---

## 🔧 Updated Components

| File | Description |
|------|-------------|
| `db_reader.py` | Loads all structured export fields: `IncidentReport`, `SymptomLog`, `StageLog`, `ConcussionAssessment` |
| `pdf_renderer.py` | Human-readable PDF including injury details, symptoms, and context |
| `epic_writer.py` | Machine-readable FHIR `Bundle` of `Observations` with metadata |
| `export_summary.py` | Assembles output, uploads PDF to Azure, returns signed URL and FHIR payload |

---

## 📄 PDF Summary Template

```
Clinical Summary – Concussion Recovery Tracker
-------------------------------------------------
User ID: abc123
Export Time: 2025-05-12T16:00:00Z

Injury Date: 2025-04-01
Reporter Role: coach
Sport: soccer
Age Group: U16
Incident Context: during match
Cleared to Play: False
Lost Consciousness: False
Diagnosed Concussion: True
Still Symptomatic: True
Seen Provider: True

Current Recovery Stage: stage_2

Symptom History:
- 2025-05-10 | headache (3) – coach
  Notes: still ongoing, worse in morning
- 2025-05-08 | dizziness (2) – coach
  Notes: improving
```

---

## 💊 FHIR Bundle Sample Output

```json
{
  "resourceType": "Bundle",
  "type": "collection",
  "entry": [
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {"text": "headache"},
        "valueInteger": 3,
        "effectiveDateTime": "2025-05-10T14:00:00Z",
        "note": [{"text": "still ongoing, worse in morning"}],
        "extension": [
          {"url": "reporter", "valueString": "coach"},
          {"url": "incident_context", "valueString": "during match"},
          {"url": "sport_type", "valueString": "soccer"},
          {"url": "age_group", "valueString": "U16"},
          {"url": "team_id", "valueString": "team123"}
        ]
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {"text": "Inferred Recovery Stage"},
        "valueString": "stage_2",
        "effectiveDateTime": "2025-05-10T15:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {"text": "Concussion Assessment Summary"},
        "valueString": "moderate risk of prolonged recovery",
        "effectiveDateTime": "2025-05-10T15:00:00Z"
      }
    }
  ]
}
```

---

## ✅ Result
- Export is now deeply contextual and clinically traceable
- PDF and FHIR both reflect real-time data in schema
- Azure upload supported with signed links for download or EHR sharing