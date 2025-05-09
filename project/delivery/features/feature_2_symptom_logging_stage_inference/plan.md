## 🧭 Feature Area 2: Symptom Logging + Stage Inference – Plan

### 🎯 Goal
Enable users to log physical, emotional, cognitive, and sleep-related symptoms and determine their recovery stage based on time since injury and severity.

### 📌 Scope

- Design and implement tools to:
  - Capture symptom check-ins
  - Store them with timestamp, injury date, user metadata
  - Infer recovery stage using `stage_engine`
- Integrate with `stage_engine.infer_stage()` logic from FA6
- Prepare data for visualization/export in FA5

#### ✅ In-Scope DB Work
- Define and implement schemas/models for:
  - Symptom log table (check-ins)
  - Tracker metadata table (injury date, last stage, cleared_to_play flag)
- Implement in Pydantic and basic persistence layer
- Mock test DB or in-memory SQLite

#### ❌ Out of Scope (handled in other Feature Areas)
- Wearable integration → Feature Area 4
- Longitudinal dashboards or charts → Feature Area 5
- Azure SQL export pipeline → Feature Area 5
- Multi-user identity & access control → Feature Area 8

### 📂 Outputs
| Phase   | Output Files |
|---------|------------------------------|
| Plan    | `plan.md`, `task_list.md` |
| Design  | `design.md`, `schema_notes.md` (if needed) |
| Build   | `symptom_logger.py`, `get_stage_guidance.py`, `app/models/symptoms.py`, `tests/` |
| Deploy  | Update schema validator if symptoms.yaml used |
| Test    | Unit tests for input parsing, stage mapping, data persistence |

### ✅ Alignment
- App Features: 2 (Recovery stage logic), 5 (Dashboard export)
- Architecture: Tracker DB, YAML input (reference/symptoms_*.yaml), FastAPI tools

### 🔗 Dependencies
- Uses `stage_engine` from Feature 6
- Uses YAML inputs from `reference/symptoms_*.yaml`
- Needs DB schema for `symptom_log` and `tracker_state`

### 🛠️ Assumptions
- Users will interact via Custom GPT, which builds tracker state in memory
- Each check-in includes timestamp, injury date, and symptom severity scores
- Symptoms will be scored on a common 0–5 scale
- `symptom_severity_max` in `stage_engine` is computed from these

### 📋 Initial Tasks
- [ ] Commit this plan
- [ ] Draft and commit `task_list.md`
- [ ] Write design spec including data model and tool flow
- [ ] Define DB schema and models
- [ ] Implement `symptom_logger.py` and `get_stage_guidance.py`
- [ ] Add tests for end-to-end stage inference
