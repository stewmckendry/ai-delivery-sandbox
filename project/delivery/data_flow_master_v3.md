## Data Flow Master (v3)

This document captures the refined backend data flows for all user actions supported by ConcussionGPT.

---

### 🔵 Triage Flow
**Tools**: `get_triage_flow`, `log_incident_detail`
**Tables**:
- `triage_response_export` — question/answer audit
- `incident_report_export` — core incident metadata
- `symptom_log_export` — symptom + score per row

**Flow**:
1. Load YAML from `triage_map.yaml`
2. GPT guides user through each prompt
3. GPT compiles `answers` → logs them via `log_incident_detail`
4. Tool stores into all 3 tables atomically

---

### 🔴 Symptom Assessment
**Tool**: `assess_concussion`
**Tables**: `concussion_assessment_export`

**Flow**:
- Reads latest symptoms from `symptom_log_export`
- Uses YAML risk tags to flag red, high, moderate symptoms
- Stores summary and red flag status

---

### 🟡 Symptom Follow-up
**Tools**: `get_symptom_log_map`, `log_symptoms`
**Tables**: `symptom_log_export`

**Flow**:
- GPT loads symptom follow-up guidance map
- User rates symptom severity + adds notes
- Each row = 1 symptom instance (w/ `score`, `notes`, `input`, `id`)

---

### 🟢 Stage Inference
**Tool**: `get_stage_guidance`
**Tables**: `stage_result_export`, `recovery_check_export`

**Flow**:
- Pulls incident and symptom data from DB
- Optional override with `quick_answers`
- Inferred stage is logged + returned

---

### ⚪ Clinical Export
**Tool**: `export_summary`
**Tables Read**: all above
**Output**: FHIR bundle + PDF (Azure Blob link)

---

### ⚫ Admin Queries
**Tool**: `get_linked_symptoms/{user_id}`
**Tables**: `symptom_log_export`
**Flow**: Returns JSON of all symptom logs chronologically

---

Every endpoint, log, and summary is linked to a real-time SQL schema and YAML ruleset. Each tool builds on earlier data, creating a full journey from incident to export.