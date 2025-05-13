## Tool Catalog (v3)

This catalog defines the available tools used by ConcussionGPT, with updated schemas, logic, and usage guidance.

---

### 1. `get_triage_flow`
- **Purpose**: Load all triage questions
- **GPT Behavior**: Walk user through prompts one-by-one
- **Special Logic**: Skip questions using `skip_if`, probe/clarify vague responses
- **Dependencies**: `triage_map.yaml`

### 2. `log_incident_detail`
- **Purpose**: Log completed triage
- **Inputs**: `user_id`, `timestamp`, `answers`
- **Answers**: Must include symptom severity dictionary (e.g., `{ "headache": 7 }`)
- **DB Writes**: `IncidentReport`, `SymptomLog`, `TriageResponse`

### 3. `assess_concussion`
- **Purpose**: Detect red flags and evaluate likelihood of concussion
- **Inputs**: `user_id`
- **Backed by**: YAML risk metadata
- **DB Writes**: `ConcussionAssessment`

### 4. `log_symptoms`
- **Purpose**: Log new or follow-up symptoms
- **Inputs**: `user_id`, `timestamp`, `symptoms` array
- **GPT Behavior**:
  - Ask: “Are you feeling [symptom] today?”
  - If yes: “How much on a 1–10 scale?”
  - Include `notes` if provided
- **DB Writes**: `SymptomLog`

### 5. `get_stage_guidance`
- **Purpose**: Infer recovery readiness
- **Inputs**: `user_id`, optional `quick_answers` for users without triage
- **Logic**: Reads `SymptomLog`, `IncidentReport`, and `RecoveryCheck`
- **DB Writes**: `StageLog`, `RecoveryCheck`

### 6. `export_summary`
- **Purpose**: Export summary as PDF + FHIR JSON
- **Inputs**: `user_id`
- **Returns**: Azure Blob URL and FHIR document

### 7. `get_linked_symptoms/{user_id}`
- **Purpose**: Retrieve all symptom logs for a user
- **Returns**: Array of { symptom_id, input, score, notes, timestamp }

### 8. `get_symptom_log_map`
- **Purpose**: Provide structured flow for follow-up check-ins
- **Contents**: Symptom categories, scoring instructions, metadata hints

---

Each tool is backed by robust schema validation and instructions to guide GPT interactions clearly and safely.