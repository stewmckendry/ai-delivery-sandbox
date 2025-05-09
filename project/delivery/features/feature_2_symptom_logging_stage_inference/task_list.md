## ✅ Task Checklist – Feature 2: Symptom Logging + Stage Inference

This tracks all major outputs and steps for delivering this feature area.

| Task | Description | Status |
|------|-------------|--------|
| Plan | Define goal, scope, outputs, dependencies | ✅ Done
| task_list.md | Track delivery steps for transparency | ✅ Done (this file)
| Design spec | Document data flows, inputs, outputs, assumptions | ✅ Done
| schema_notes.md | Clarify YAML and DB schemas (if needed) | ✅ Done
| symptom_logger.py | Tool to log symptoms and build tracker state | ✅ Done
| get_stage_guidance.py | Tool to run stage_engine on current state | ✅ Done
| models/symptoms.py | Define symptom scoring models (0–5) | ✅ Done
| models/tracker.py | Extend with symptom log fields | ✅ Done
| DB schema | Design tables for symptom_log and metadata | ✅ Done
| Unit tests | Validate tools and models | ✅ Done
| validator updates | Add YAML validation for symptoms_* (optional) | ⬜ Not Started
| DB write integration | Add real persistence layer to symptom_logger | ⬜ Not Started
| Tool contracts notes | Document GPT schema guidance | ✅ Done
| Symptom scoring enhancement | Add weighted scoring / categorization → Feature 5 | ⬜ Not Started
| Scope tracker | Update master scope log with FA2 content | ✅ Done