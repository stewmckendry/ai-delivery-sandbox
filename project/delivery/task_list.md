- [x] ✅ Refactor `triage_map.yaml` to add `skip_if`, simplify metadata, improve example answers
- [x] ✅ Update `get_triage_flow.py` to remove unused fields and simplify responses
- [x] ✅ Revise GPT system instructions for triage and symptom check-in
- [x] ✅ Refactor `assess_concussion` to pull symptoms from DB, not payload
- [x] ✅ Add `RecoveryCheck` to db_models and `get_stage_guidance` for non-triage users
- [x] ✅ Enhance guidance logic in `assess_concussion`, return red, high, moderate lists
- [x] ✅ Update `log_symptoms` to handle new symptom schema and validate entries
- [x] ✅ Refactor all OpenAPI schemas with detailed instructions, properties, examples
- [x] ✅ Ensure GPT schema responses include style and communication guidance
- [x] ✅ Align `get_symptom_log_map` with new symptom logging format
- [x] ✅ Add fallback handling to `log_incident_detail` when scores are missing
- [x] ✅ Archive unused tools (`export_to_sql`, `db_writer.py`, `validator.py`)

### Next:
- [ ] 🚧 Final round of testing all tools inside the Custom GPT config
- [ ] 🔍 Review GPT behavior across full triage > assess > log > stage > export journey
- [ ] 📘 Write deployment checklist to finalize handoff
- [ ] 🧪 Design test coverage plan (unit + user flow)
- [ ] 🧹 Clean-up: remove placeholder tasks, deprecated fields, and unused metadata