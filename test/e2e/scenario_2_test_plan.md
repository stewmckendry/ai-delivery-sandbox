# 🧪 Scenario 2: End-to-End Return-to-Play Test Plan

**Goal:** Validate the full user journey from triage through concussion assessment, stage education, activity check-ins, and export.

---

### 🧠 Scenario Setup
- **User ID:** user_003
- **Context:** Youth soccer player, mild symptoms, no prior diagnosis
- **Injury Date:** 2025-05-10

---

### 🔁 Flow Steps

1. **Start Triage**
- Tool: `get_triage_flow`
- Expected: Load full triage questions

2. **Walk Through Triage Questions**
- Confirm: Responses are saved and follow logic (probe/clarify/skip_if)

3. **Log Incident**
- Tool: `log_incident_detail`
- Expected: Write structured answers including symptoms to SQL

4. **Assess Concussion**
- Tool: `assess_concussion`
- Expected: Red flags evaluated, moderate symptoms detected if present

5. **Explain Return-to-Play Stages**
- Tool: `get_stage_overview`
- Expected: GPT can explain stage names, activities, and criteria

6. **Check-in Day 1**
- Tool: `get_checkin_flow` → `log_activity_checkin`
- Expected: Logs activity attempt and symptom experience

7. **Get Stage Guidance**
- Tool: `get_stage_guidance`
- Expected: Should confirm current stage (e.g., stage_1), with reasoning

8. **Check-in Day 2 (Progress)**
- Same tools
- Should progress to stage_2 if symptoms mild and 24h passed

9. **Check-in Day 3 (Worsening)**
- Simulate worsened symptoms
- Expect: regression to prior stage

10. **Export Summary**
- Tool: `export_summary`
- Expected: PDF and FHIR outputs with full journey (incident, symptoms, stage logic, activity)

---

### ✅ Verification
- Use Azure Data Studio to confirm DB entries:
  - `incident_report_export`
  - `symptom_log_export`
  - `activity_checkin_export`
  - `stage_result_export`
- Confirm PDF shows stage, activities, and check-in results
- Confirm FHIR includes all bundles

---

🔚 Close scenario after verifying fallback logic, progression, and regression all handled
