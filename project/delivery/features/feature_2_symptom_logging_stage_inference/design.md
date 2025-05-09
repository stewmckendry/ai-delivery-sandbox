## 🔪 Feature Area 2: Symptom Logging + Stage Inference – Design

### 🔍 Purpose
This design supports daily or periodic symptom logging via a conversational agent and automatically infers recovery stage based on severity and time since injury.

### 🧹 Modules

#### `symptom_logger`
- **Purpose**: Accepts check-in data, validates and updates tracker state
- **Called by**: GPT tool `log_symptoms`
- **Uses**: `symptoms.yaml` for categories + metadata
- **Writes to**: SQLite (symptom_log), tracker state
- **Input Schema**:
```python
SymptomCheckIn(BaseModel):
    user_id: str
    injury_date: date
    checkin_time: datetime
    symptoms: Dict[str, int]  # id → 0-5
```
- **Output Schema**:
```python
SymptomLogResult(BaseModel):
    tracker_state: TrackerState
    message: str
```
- **Assumptions**: GPT handles question prompting and yields a full check-in payload

#### `get_stage_guidance`
- **Purpose**: Uses stage_engine to infer stage from symptom log
- **Called by**: GPT tool after symptom logging or on demand
- **Input Schema**:
```python
StageInferenceRequest(BaseModel):
    user_id: str
    tracker_state: TrackerState
```
- **Output Schema**:
```python
StageInferenceResult(BaseModel):
    stage_result: StageResult
    message: str
```
- **Assumptions**: Pulls symptoms + injury date from recent tracker state, computes stage

### 💃 DB Schema
- `symptom_log`: user_id, timestamp, symptoms (JSON), source, stage_inferred
- `tracker_state`: user_id, injury_date, last_stage, last_checkin_time

### ⚙️ Flow Summary
1. GPT gathers symptoms via Custom GPT UI
2. `log_symptoms` sends to `symptom_logger`
3. Tracker state is updated, check-in is logged
4. `get_stage_guidance` sends symptoms to `stage_engine`
5. Returns current recovery stage and guidance to user

### 📌 Traceability
- App Feature: 2 (Recovery stage logic)
- Architecture: YAML+Tracker state+FastAPI+SQLite
- YAML Inputs: `reference/symptoms_*.yaml`
- Engine: `stage_engine.infer_stage()`

### 🧱 Builder Notes
- Add `SymptomCheckIn` and `SymptomLogResult` to `models/symptoms.py`
- Update `models/tracker.py` for `TrackerState`
- Write both tools with FastAPI tool wrapper and OpenAPI schema
- Log test entries to mock DB or in-memory file

### 🧠 Assumptions
- All symptoms scored on 0–5 scale
- GPT produces validated symptom map by ID
- `stage_engine` can handle empty or low-symptom input gracefully
