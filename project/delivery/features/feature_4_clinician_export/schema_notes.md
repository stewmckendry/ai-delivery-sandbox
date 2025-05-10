## 📘 schema_notes.md – FHIR Export for Feature 4

### 🧠 FHIR Overview (For Non-Experts)
FHIR (Fast Healthcare Interoperability Resources) is a standard for exchanging healthcare data electronically. Each type of medical record is represented as a **Resource**:
- **Condition** – the diagnosis (e.g., "Concussion")
- **Observation** – tracked data points (e.g., symptoms, severity)
- **CarePlan** – what the user is advised to do (e.g., rest, return-to-play guidance)

FHIR resources are sent as part of a **Bundle**, a JSON wrapper containing multiple records in a standard structure.

---

### 📦 Example Bundle Output
```json
{
  "resourceType": "Bundle",
  "type": "collection",
  "entry": [
    { "resource": { /* Condition resource */ } },
    { "resource": { /* Observation: headache */ } },
    { "resource": { /* Observation: dizziness */ } },
    { "resource": { /* CarePlan resource */ } }
  ]
}
```

---

### 📄 Condition (Diagnosis: Concussion)
```json
{
  "resourceType": "Condition",
  "clinicalStatus": {
    "coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
      "code": "active"
    }]
  },
  "code": {
    "coding": [{
      "system": "http://snomed.info/sct",
      "code": "71904000",
      "display": "Concussion"
    }]
  },
  "subject": {"reference": "Patient/example"},
  "recordedDate": "2025-04-01"
}
```

---

### 📄 Observation (Symptom: Headache)
```json
{
  "resourceType": "Observation",
  "code": {
    "text": "Headache Severity"
  },
  "valueInteger": 3,
  "subject": {"reference": "Patient/example"},
  "effectiveDateTime": "2025-04-01T10:00:00Z"
}
```
(Repeat for each symptom log. Could include duration, trend, or stage tag.)

---

### 📄 CarePlan (Recovery Guidance)
```json
{
  "resourceType": "CarePlan",
  "status": "active",
  "intent": "plan",
  "title": "Concussion Recovery Plan",
  "description": "Rest, reduce screen time, and follow stage guidance",
  "subject": {"reference": "Patient/example"},
  "period": {
    "start": "2025-04-01",
    "end": "2025-04-07"
  }
}
```

---

### 🔧 Notes for Implementation
- We'll assemble these via `epic_writer.py`
- All fields will be programmatically generated from the tracker + symptom DB
- We'll validate against a lightweight FHIR schema (no full HL7 check initially)
- Aim for clear, reproducible JSON that can be sent to Epic sandbox

Let me know if you'd like a visual diagram or a side-by-side YAML→FHIR mapping view!