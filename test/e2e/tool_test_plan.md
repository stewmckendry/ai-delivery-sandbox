## Tool Test Plan: Concussion Recovery Assistant (E2E Tool Coverage)

### ✅ Triage Tools

**/get_triage_flow**
- [ ] Returns full triage map with expected schema fields
- [ ] `skip_if` and `symptom_links` behavior confirmed

**/get_triage_question**
- [ ] Correct next question after given tracker state
- [ ] Handles completion (no remaining questions)

**/log_incident_detail**
- [ ] Correctly logs structured answer payloads
- [ ] Symptom map accepted, validated, and saved
- [ ] Invalid or missing fields raise useful errors

### ✅ Assessment Tools

**/assess_concussion**
- [ ] Detects red flags, high-risk, and moderate-risk symptoms
- [ ] Outputs correct `concussion_likely` flag + summary
- [ ] Handles missing symptoms gracefully

**/get_stage_guidance**
- [ ] Computes stage from injury + symptoms correctly
- [ ] Graceful fallback when symptoms or date missing
- [ ] Summary language clear and aligned with guidance phrases

### ✅ Symptom Tracking Tools

**/get_symptom_log_map**
- [ ] Loads YAML structure correctly
- [ ] Guidance and escalation logic works

**/log_symptoms**
- [ ] Stores symptoms, severity, and optional notes
- [ ] Unknown symptom names logged as `other`
- [ ] Validates and maps symptom inputs

**/get_linked_symptoms**
- [ ] Returns history log of symptom entries
- [ ] Includes scores, notes, timestamps

### ✅ Export Tools

**/export_summary**
- [ ] Generates valid PDF URL
- [ ] Includes recent symptoms, triage, stage
- [ ] Builds valid FHIR bundle

---

Next: Create end-to-end test user flows to validate full lifecycle from triage to export.