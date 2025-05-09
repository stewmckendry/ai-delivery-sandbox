## ✅ Task Checklist – Feature 6: YAML Engines

This tracks all major outputs and steps for delivering the YAML Engines feature.

| Task | Description | Status |
|------|-------------|--------|
| Design Spec | Document requirements, flows, schemas | ✅ Done
| triage_engine.py | Engine for loading and querying triage map | ✅ Done
| stage_engine.py | Engine for stage inference using symptoms | ✅ Done
| schema_validator.py | CI tool to validate YAMLs | ⬜ Not Started
| Triage schemas | `app/models/triage.py` | ✅ Done
| Stage schemas | `app/models/stage.py` | ✅ Done
| Tracker state schema | `app/models/tracker.py` | ✅ Done
| YAML explainer doc | Descriptions and usage of YAML-based flows | ✅ Done
| Unit tests | Test `triage_engine.py` logic | ✅ Done
| CI validator script | Lint YAML and enforce changelog entries | ⬜ Not Started

🔜 To Do:
- Handle `symptom_severity_max` scoring logic — proposed to be implemented in Feature Area 2 (Symptom Logging & Stage Inference). This will define how symptom values are captured and translated into numeric scores for engine input.