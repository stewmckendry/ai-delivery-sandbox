# 📘 Stage Guidance Architecture (get_stage_guidance Tool)

## 🎯 Purpose
The `/get_stage_guidance` tool infers a user's current recovery stage using recent symptom scores and injury timing. It implements logic aligned with SCAT6 Return-to-Play (RTP) stages, returning a recommendation and storing the result for clinical or tracking use.

---

## 🔄 Inputs
- `user_id`: Unique ID for the user
- `injury_date`: Optional override (else fetched from DB)
- `symptoms`: Optional override as `{ symptom_id: score }`
- `checkin_time`: Optional timestamp (defaults to now)

If not supplied, the tool fetches:
- `injury_date` from `IncidentReport`
- Recent `SymptomLog` entries (last 10)

---

## 🧠 Logic Flow
1. **Input Validation**
   - Ensures either symptoms and injury date are passed or can be fetched.

2. **Logging (RecoveryCheck)**
   - If override inputs are used, logs them in `recovery_check` table.

3. **Stage Inference (StageEngine)**
   - Loads `reference/stages.yaml`, parsed into a `StageMap`
   - Calculates:
     - `days_since_injury`
     - `symptom_severity_score = sum(symptoms.values())`
   - For each stage:
     - Checks `duration_min_hours`
     - Compares against `symptom_severity_max` (must be ≤ cutoff)
     - Returns first matching stage with `guidance`, `label`, and `matched_criteria`

4. **Logging (StageLog)**
   - Saves result to `stage_result_export`

---

## 🧪 SCAT6 Alignment
Each YAML stage models a SCAT6 return-to-play milestone:
- Stage 1: Symptom-limited activity
- Stage 2: Light aerobic
- Stage 3–6: Gradual return to team, contact, and full play

Progression rules encoded in:
```yaml
stage_criteria_logic:
  symptom_severity_max: "mild"
  duration_min_hours: 24
```
These enforce a minimum recovery time and symptom resolution.

---

## 🧑‍💻 Developer Notes
- `StageMap` and `StageResult` are validated Pydantic models
- `symptom_severity_max` values must be one of: `mild`, `moderate`, `severe`
- Logs include structured criteria match for transparency

---

## 📁 Files
- Tool: `app/tools/get_stage_guidance.py`
- Engine: `app/engines/stage_engine.py`
- YAML Config: `reference/stages.yaml`
- DB Models: `StageLog`, `RecoveryCheck`

---

## 🧩 Future Ideas
- Allow symptom trend weighting
- Make progression criteria user-configurable
- Integrate provider override flow