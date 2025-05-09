## ✍️ Design Spec – Feature Area 6: YAML Engines

### 🔍 Scope
Design the core YAML parsing and validation logic for:
- `triage_engine.py` – traverses triage map logic, returns next question, flags red flags
- `stage_engine.py` – infers recovery stage using symptoms and durations
- `schema_validator.py` – validates structure and fields in YAML inputs

All engines will:
- Load YAMLs from `reference/`
- Validate format using `pydantic` models
- Return typed objects or raise validation errors

---

## 🧩 Module: `app/engines/triage_engine.py`

### 🔗 App Feature Alignment
- Supports: Structured Triage & Assessment (App Feature 1)

### 🔄 User Journey Context
- **Initial Entry Point:** `get_triage_flow` is called once at the start of a triage interaction. It loads the entire triage map so GPT can guide the conversation fluidly without backend calls for each question.
- **Per-Turn Logic (optional path):** `get_triage_question` may be used instead of `get_triage_flow` if a step-by-step mode is desired. It uses current state to return the next question only.
- **Conclusion:** Once the user has completed the triage, `assess_concussion` is called. It uses the full tracker state (user's answers) and calls `triage_engine.evaluate_flags()` to:
  - Identify red flags (via `red_flag_check`)
  - Summarize user input to determine likelihood of concussion

**Tool Coordination:**
1. `get_triage_flow` → GPT loads triage map
2. GPT guides user and builds up `tracker_state`
3. `assess_concussion` → uses final state to evaluate red flags and assess concussion

### 📥 Input Schema
```python
class TrackerState(BaseModel):
    current_node_id: str
    answers: Dict[str, str]
```

### 📤 Output Schema
```python
class QuestionOutput(BaseModel):
    question: str
    options: List[str]
    is_terminal: bool

class FlagOutput(BaseModel):
    red_flags: List[str]
```

### 📌 Assumptions
- `triage_map.yaml` is valid and includes well-formed stages and questions
- Tracker state is persisted and built up by GPT in memory, then passed to tools for evaluation
- Responses are stored to the DB (SQLite/Azure SQL) for logging and downstream analysis

### 🛠️ Builder Guidance
- Support reloading on change for dev ease
- Handle missing nodes, circular refs with clear errors

### Responsibilities
- Load and parse `triage_map.yaml`
- Given a `tracker_state`, return next question, options
- Evaluate `red_flag` symptoms

### Pydantic Schema (`app/models/triage.py`)
```python
class TriageQuestion(BaseModel):
    id: str
    prompt: str
    type: str
    intent: Optional[str]
    mode: Optional[str]
    response_parsing: Optional[str]
    symptom_links: Optional[List[str]]
    red_flag_check: Optional[bool] = False
    tool_tags: Optional[List[str]]
    example_user_answers: Optional[List[str]]
    followup_conditions: Optional[List[Dict[str, Any]]]

class TriageStage(BaseModel):
    id: str
    name: str
    description: Optional[str]
    questions: List[TriageQuestion]

class TriageMap(BaseModel):
    triage_flow: List[TriageStage]
```

### Output
```python
TriageEngine.get_next_question(tracker_state: dict) -> dict
TriageEngine.evaluate_flags(tracker_state: dict) -> List[str]
```

---

## 🧩 Module: `app/engines/stage_engine.py`

### 🔗 App Feature Alignment
- Supports: Recovery Stage Logic (App Feature 2)

### 🔄 User Journey Context
- **Symptom Check-in:** User logs symptoms through `update_symptoms`. These are passed along with injury date into `get_stage_guidance`.
- **Stage Evaluation:** `get_stage_guidance` calls `stage_engine.infer_stage()` to assess recovery stage.
- **Result Usage:**
  - GPT surfaces return-to-play guidance based on result.
  - `get_tracker_status` may display current stage with criteria match.

**Tool Coordination:**
1. `update_symptoms` → collects symptoms and days_since_injury
2. `get_stage_guidance` → returns guidance from stage engine
3. `get_tracker_status` → shows user progress and stage logic match

### 📥 Input Schema
```python
class StageInput(BaseModel):
    symptoms: Dict[str, int]  # symptom ID → severity
    days_since_injury: int
```

### 📤 Output Schema
```python
class StageResult(BaseModel):
    stage_id: str
    label: str
    guidance: str
    matched_criteria: Dict[str, Any]
```

### 📌 Assumptions
- `symptoms_*.yaml` provide structured metadata per symptom group
- `stages.yaml` defines criteria for stage entry, including duration and severity thresholds
- Symptoms and recovery tracker states are stored in the database for longitudinal tracking

### 🛠️ Builder Guidance
- Build `infer_stage()` to return first-matching stage
- Log criteria evaluated per stage for trace/debug

### Responsibilities
- Load `stages.yaml` and `symptoms_*.yaml`
- Assess current stage based on symptoms and duration
- Provide return-to-play recommendations

### Pydantic Schema (`app/models/stage.py`)
```python
class StageCriteriaLogic(BaseModel):
    min_days: int
    max_days: int
    symptoms_threshold: int

class StageDefinition(BaseModel):
    id: str
    name: str
    description: Optional[str]
    stage_number: int
    allowed_activities: List[str]
    contraindicated_examples: List[str]
    guidance_phrases: List[str]
    stage_criteria_logic: StageCriteriaLogic
    medical_clearance_required: bool

class StageMap(BaseModel):
    stages: List[StageDefinition]
```

### Output
```python
StageEngine.infer_stage(symptoms: dict, days_since_injury: int) -> dict
```

---

## 🧪 Module: `app/engines/schema_validator.py`

### 🔗 App Feature Alignment
- Supports: YAML Engines and CI Validation (App Features 6 & 7)

### 🔄 User Journey Context
- **During Dev:** Developers run schema validator on modified YAMLs during feature build
- **During CI:** Validator is called as a CI job or pre-commit hook to block malformed data
- **Outcome:** Prevents schema drift, invalid inputs, and ensures changelog entries are enforced

### 📥 Input Schema
```python
class FileValidationTask(BaseModel):
    path: str
    schema_type: Literal['triage', 'stage', 'symptom']
```

### 📤 Output Schema
```python
class ValidationResult(BaseModel):
    success: bool
    errors: Optional[List[str]]
```

### 📌 Assumptions
- Schemas are maintained in `app/models/`
- Files follow filename convention to detect type automatically

### 🛠️ Builder Guidance
- Add CLI flags: `--file`, `--all`, `--changelog`
- Raise or exit non-zero on failure in CI context

### Responsibilities
- Validate each YAML input file against its schema
- Enforce required fields and structure
- Log changelog entries when schemas evolve

### CLI Entry (to be run in CI)
```bash
python app/engines/schema_validator.py --all
```

### Output
- Validated data or exception with helpful message
- Summary log of results

---

## 🔗 Tools Supported
These engines will be used by:
- `get_triage_question`, `get_triage_flow`, `assess_concussion` (via `triage_engine`)
- `get_stage_guidance`, `get_tracker_status` (via `stage_engine`)

---

## 📁 File Paths
- Engines:
  - `app/engines/triage_engine.py`
  - `app/engines/stage_engine.py`
  - `app/engines/schema_validator.py`
- Models:
  - `app/models/triage.py`
  - `app/models/stage.py`
- YAML Inputs: `reference/*.yaml`

---

## 🧠 Next Steps
- Implement `TriageEngine` and `StageEngine` classes with schema-based loaders
- Write unit tests for each engine (triage: branching; stage: criteria match)
- Build validator CLI and test in `test/infra/`