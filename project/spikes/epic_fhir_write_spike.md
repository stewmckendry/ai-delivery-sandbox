## 🧪 Spike Report: Epic FHIR Write Access – Concussion Recovery GPT App

---

### 🎯 Objective
Test whether our backend can write structured medical data to the Epic FHIR sandbox via the Observation resource. This validates the feasibility of automated clinical data sharing from the GPT app.

---

### 🧭 Plan Summary

#### ✅ Success Criteria
- Authenticate using OAuth 2.0 (client credentials)
- POST an `Observation` resource to the Epic sandbox
- Receive a `201 Created` response with a valid resource ID

#### 🔧 Scope
- Focus only on `Observation.write`
- Use mock vitals (e.g., symptom score or recovery stage)
- No user-level consent flow (handled separately in real integrations)

---

### 🛠️ Setup Steps (Documented for Reuse)

#### 1. Create Developer Account
- URL: [https://fhir.epic.com/](https://fhir.epic.com/)
- Register a new application → Copy `Client ID` and `Client Secret`
- Select scopes: `patient/Observation.write`, `offline_access`, `openid`

#### 2. Get OAuth 2.0 Token

```bash
curl -X POST \
  https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=client_credentials&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET'
```

- ✅ Success = JSON response with `access_token`
- 🔁 Valid for ~60 minutes; reuse for test calls

#### 3. POST Observation Resource

```bash
curl -X POST \
  https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Observation \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/fhir+json" \
  -d @observation_payload.json
```

##### Example Payload (observation_payload.json)
```json
{
  "resourceType": "Observation",
  "status": "final",
  "code": {
    "coding": [{
      "system": "http://loinc.org",
      "code": "55284-4",
      "display": "Blood pressure systolic and diastolic"
    }],
    "text": "Symptom burden score"
  },
  "subject": {
    "reference": "Patient/example"
  },
  "effectiveDateTime": "2025-05-01T10:00:00Z",
  "valueQuantity": {
    "value": 5,
    "unit": "score",
    "system": "http://unitsofmeasure.org",
    "code": "1"
  }
}
```

---

### ✅ Results
- Authenticated successfully and retrieved token
- POSTed observation → received `201 Created`
- Resource included a new `Observation.id` → visible in patient summary via sandbox tools

---

### 📌 Conclusion & Next Steps
- ✅ Feasible to push clinical summaries (Observation, Condition) to Epic
- 🔐 App registration + token exchange adds 1 step but can be automated in FastAPI
- 🧠 Use `export_summary` tool to call this logic for clinician exports

---

### 📂 Output Files to Implement
- `epic_client.yaml` – store client ID/secret in backend config
- `epic_writer.py` – helper function to send FHIR JSON to Epic
- Extend `export_summary` tool to support optional FHIR export

This pattern is reusable for other FHIR resources in future phases.