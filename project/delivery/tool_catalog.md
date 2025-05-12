## 🧰 GPT Tool Catalog – Concussion Recovery App

This catalog outlines the tools available for use by the Custom GPT to manage triage, symptom tracking, recovery assessment, and data export.

---

### 🧭 1. Triage Tools

#### `get_triage_flow`
- **Purpose:** Load the full YAML-driven triage map to guide GPT dialog
- **When to Use:** At the start of triage, to understand the full question flow
- **Input:** None
- **Output:** JSON of all triage stages/questions from `triage_map.yaml`
- **Note:** Enables GPT to plan conversation sequence. Each question includes `mode_description` to inform how to ask and `symptom_links` to guide which symptoms to listen for.

#### `get_triage_question`
- **Purpose:** Return the next unanswered question
- **When to Use:** To progress sequentially through questions
- **Input:** TrackerState.answers so far
- **Output:** Next question (prompt, type, id)
- **Note:** Alternative to above if GPT isn't managing state fully

#### `log_incident_detail`
- **Purpose:** Store triage answers into TrackerMetadata
- **When to Use:** After triage conversation is complete
- **Input:** user_id, answers dict
- **Output:** success message
- **Note:** Answers stored as JSON for future reuse. Also sets up metadata for use in later tools.

#### `assess_concussion`
- **Purpose:** Evaluate answers and infer red flags & stage
- **When to Use:** After triage questions answered
- **Input:** TrackerState
- **Output:** TrackerState with stage, red flags, cleared_to_play
- **Note:** Uses YAML-based logic in `triage_engine` + `stage_engine`

---

### 🧾 2. Symptom Tools

#### `log_symptoms`
- **Purpose:** Log symptom check-in and persist state
- **When to Use:** After user completes daily check-in
- **Input:** SymptomCheckIn (symptoms + metadata)
- **Output:** TrackerState
- **Note:** Looks up missing metadata from `TrackerMetadata` if not included in payload. Persists via `log_symptoms_to_db`.

#### `get_stage_guidance`
- **Purpose:** Infer recovery stage and suggest next steps
- **When to Use:** Post-symptom check-in
- **Input:** TrackerState
- **Output:** StageResult (current stage, clearance info)

---

### 📦 3. Export + Reporting

#### `export_summary`
- **Purpose:** Generate and store PDF + FHIR bundle
- **When to Use:** On user or clinician request
- **Input:** user_id
- **Output:** PDF contents (or storage URL), FHIR bundle
- **Note:** PDF and FHIR files are written locally and uploaded to Azure Blob using `upload_to_storage`.

#### `export_to_sql`
- **Purpose:** Push anonymized data to analytics database
- **When to Use:** On schedule or manual trigger
- **Input:** None
- **Output:** None (writes to SQL DB)

---

### 🤖 GPT Flow Guidance

- **Natural Flow Option**:
  - Use `get_triage_flow` once
  - Ask questions conversationally
  - On complete: `log_incident_detail` → `assess_concussion`

- **Fallback Flow Option**:
  - Repeatedly call `get_triage_question`
  - Log via `log_incident_detail` after each
  - Call `assess_concussion`

This catalog should be kept in sync with tool implementation and GPT prompt examples.