## 🧠 Addendum – Stage Criteria Logic

This note explains the schema used in `stages.yaml` for determining recovery stages.

---

### 🔹 `stage_criteria_logic`
Defines logic for inferring whether a user qualifies for a recovery stage.

#### 🔸 Schema Definition (in `app/models/stage.py`):
```python
class StageCriteriaLogic(BaseModel):
    symptom_severity_max: Literal["mild", "moderate", "severe"]  # Maximum allowed symptom score severity
    duration_min_hours: int  # Required minimum time since injury
```

#### 🔸 Example YAML Usage
```yaml
stage_criteria_logic:
  symptom_severity_max: "mild"
  duration_min_hours: 24
```

#### 🔸 Logic Interpretation (used in `stage_engine.py`):
```python
severity_score = sum(symptoms.values())
SEVERITY_CUTOFFS = {"mild": 5, "moderate": 10, "severe": 15}

if hours_since_injury >= logic.duration_min_hours and severity_score <= SEVERITY_CUTOFFS[logic.symptom_severity_max]:
    # stage matched
```

#### 🔸 Used By:
- `stage_engine.infer_stage()` → returns `StageResult`
- `get_stage_guidance` → tool using result to guide user

### 📌 Summary
- The logic allows for threshold-based stage matching
- Easy to evolve: can support advanced scoring later (e.g., symptom weighting, NLP parsing)
- YAML-first model lets content be tuned by domain experts without engine changes

---