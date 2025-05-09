## 📘 Schema Addendum – Feature 6: YAML Engine Context

### 🧠 Overview
This addendum explains key YAML-based schema concepts used in the triage and stage engines.

---

### 🔹 Triage Map (YAML: `triage_map.yaml`)
- **Purpose:** Defines the full structure and logic of the triage conversation.
- **Schema:** `TriageMap`, `TriageStage`, `TriageQuestion` (see `app/models/triage.py`)
- **Used By:** `triage_engine.py`, tools `get_triage_flow`, `get_triage_question`, `assess_concussion`
- **Content:**
  - List of stages, each with a name and questions
  - Questions define prompts, answer options, red-flag checks, followups

### 🔹 Tracker State (in-memory or DB)
- **Purpose:** Tracks which questions the user has answered
- **Schema:** To be defined in `app/models/tracker.py`
- **Used By:** Passed to `triage_engine`, `stage_engine`, and eventually stored to DB
- **Structure:**
```python
class TrackerState(BaseModel):
    answers: Dict[str, str]  # question_id → user answer
```

### 🔹 Stage Map (YAML: `stages.yaml`)
- **Purpose:** Logic for assigning a recovery stage
- **Schema:** `StageMap`, `StageDefinition`, `StageCriteriaLogic` (see `app/models/stage.py`)
- **Used By:** `stage_engine.py`, tool `get_stage_guidance`
- **Content:**
  - List of stages
  - Thresholds for symptoms + days since injury

### 🔹 Symptom Metadata (YAML: `symptoms_*.yaml`)
- **Purpose:** Additional context per symptom category
- **Used By:** `stage_engine.py`, optional analysis in tools

---

### 📁 Folder Reference
- YAML files: `reference/`
- Models: `app/models/`
- Engines: `app/engines/`
- Trackers: `app/models/tracker.py` (planned)

### 📌 Summary
- YAML files hold the decision logic
- Engines interpret and apply this logic
- Tracker state is the input/output flow passed between GPT and tools
- All YAMLs are validated at build-time using schemas

---