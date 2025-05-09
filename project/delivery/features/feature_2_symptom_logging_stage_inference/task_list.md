## ✅ Task Checklist – Feature 2: Symptom Logging + Stage Inference

This tracks all major outputs and steps for delivering this feature area.

| Task | Description | Status |
|------|-------------|--------|
| Plan | Define goal, scope, outputs, dependencies | ✅ Done
| task_list.md | Track delivery steps for transparency | ✅ Done (this file)
| Design spec | Document data flows, inputs, outputs, assumptions | ✅ Done
| schema_notes.md | Clarify YAML and DB schemas (if needed) | ⬜ Not Started
| symptom_logger.py | Tool to log symptoms and build tracker state | ⬜ Not Started
| get_stage_guidance.py | Tool to run stage_engine on current state | ⬜ Not Started
| models/symptoms.py | Define symptom scoring models (0–5) | ⬜ In Progress
| models/tracker.py | Extend with symptom log fields | ⬜ Not Started
| DB schema | Design tables for symptom_log and metadata | ⬜ Not Started
| Unit tests | Validate tools and models | ⬜ Not Started
| validator updates | Add YAML validation for symptoms_* (optional) | ⬜ Not Started