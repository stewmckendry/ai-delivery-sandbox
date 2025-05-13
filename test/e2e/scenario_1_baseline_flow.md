## E2E Scenario 1: Baseline Recovery Flow (Mild Symptoms, No Red Flags)

### 🎯 Goal
Test a smooth user journey from triage through to stage guidance and export with a mild, non-urgent symptom profile.

### 👤 User Context
- `user_id`: `user_mild_case`
- Reporting for: "my daughter"
- Age group: U11
- Sport: soccer
- Date of injury: 2025-05-01
- Symptoms: mild headache (2), slight dizziness (1)

### 🧪 Step-by-Step Test

#### 1. **GET /get_triage_flow**
- [ ] Fetch full triage map.
- [ ] Validate presence of `reporter_role`, `injury_context`, `symptoms`, and conditional logic.

#### 2. **POST /log_incident_detail**
- [ ] Submit structured answers including:
```json
{
  "user_id": "user_mild_case",
  "timestamp": "2025-05-13T10:00:00Z",
  "answers": {
    "reporter_role": "my daughter",
    "sport_type": "soccer",
    "age_group": "U11",
    "team_id": "Rosedale Ravens",
    "injury_date": "2025-05-01",
    "injury_context": "She bumped heads with another player",
    "symptoms": {"headache": 2, "dizziness": 1},
    "lost_consciousness": false,
    "seen_provider": true,
    "diagnosed_concussion": false,
    "still_symptomatic": true,
    "cleared_to_play": false
  }
}
```

#### 3. **POST /assess_concussion**
- [ ] Confirm that `concussion_likely` is false or mild.
- [ ] Ensure no red flags or high-risk symptoms returned.

#### 4. **POST /get_stage_guidance**
- [ ] Submit `user_id`, rely on DB to fetch symptoms.
- [ ] Expect stage 1 or 2, mild language.

#### 5. **POST /export_summary**
- [ ] Confirm PDF URL is returned.
- [ ] Validate presence of FHIR bundle.

#### 6. **GET /get_linked_symptoms/{user_id}**
- [ ] Check logged symptoms are retrievable with correct timestamps and scores.

---

### ✅ Expected Outcome
- No errors throughout.
- Smooth flow from triage to stage.
- PDF and FHIR outputs validated.

### 🧠 Notes
- This case sets the baseline for other test variations.
- Symptom IDs should match known references.
- Confirm graceful handling of optional fields.

---

Next: Run this test and report results. I’ll prepare the summary and any follow-up fixes or logs.