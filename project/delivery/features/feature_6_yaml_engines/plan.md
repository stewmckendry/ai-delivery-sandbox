## 🧠 Feature Area 6 – YAML Engines: Delivery Plan

### 🎯 Goals
- Parse and validate YAML logic for triage and stage inference
- Support red flag detection, stage guidance, and changelog/versioning
- Ensure tool contracts align with YAML schema

### 🧱 YAML Inputs (from repo)
- `reference/triage_map.yaml`
- `reference/stages.yaml`
- `reference/symptoms_physical.yaml`
- `reference/symptoms_emotional.yaml`
- `reference/symptoms_cognitive.yaml`
- `reference/symptoms_sleep.yaml`
- `reference/symptoms_red_flag.yaml`

### 🧩 Planned Engines
- `triage_engine.py` → traverse triage_map, flag risks
- `stage_engine.py` → infer stage from symptom+duration
- `schema_validator.py` → shared validator for all YAMLs

### 📋 Validation Plan
- **Runtime**: Each tool (e.g., `get_triage_question`) checks YAML structure and required fields before use
- **CI**: Validator script runs on commit to enforce schema + changelog tracking

### 📘 Tools That Use These Engines
- `get_triage_flow`, `get_triage_question`, `assess_concussion`
- `get_stage_guidance`, `get_tracker_status`

### 💡 Implementation Notes
- Use `pydantic` for YAML schema definitions
- Load YAMLs dynamically from disk (via repo folder)
- Add CI hook for validation script
- Engines return validated objects with helpful error messages