# 🧠 Triage Flow QA – Fix Task List

This task list addresses key issues surfaced during full triage testing via ConcussionGPT. Issues include flow/UX gaps, tool interface bugs, and structural schema weaknesses.

---

## 🛠 General System Fixes
- [ ] Improve error messaging across all tools (replace `UnrecognizedKwargsError` with readable errors)
- [ ] Revalidate OpenAPI schemas to match tool expectations
- [ ] Update SQL Server schema to match `db_models.py` (e.g., SymptomLog changes)

---

## ✅ Phase 1: Tool Refactors (Complete)
- [x] Refactor `symptom_logger.py` for new schema
- [x] Refactor `get_linked_symptoms.py`, `db_reader.py`
- [x] Deprecate `db_writer.py`, `validator.py`, `export_to_sql.py`
- [x] Update `assess_concussion` to pull from DB

---

## 🔁 Phase 2: Tool Enhancements
- [ ] Update `log_incident_detail.py` to also insert symptoms into `SymptomLog`
- [ ] Audit `get_stage_guidance`, `export_summary`, and `get_symptom_log_map` for refactors
- [ ] Revalidate and simplify OpenAPI + GPT instructions across all tools

---

## 🧭 Phase 3: Triage Experience Improvements

### 🧮 Question Design
- [ ] Re-audit `triage_map.yaml` for correct `mode` (`probe`, `select`, `inform`)
- [ ] Add `next_qid_if_true/false` branching logic support

### 🧪 Data Validation
- [ ] Add `enum` or `pattern` to restrict `age_group`, `sport_type`, etc.
- [ ] Normalize symptom keys using `symptom_log_map.yaml`

---

## 💬 Phase 4: GPT UX Guardrails
- [ ] Require confirmation before calling tools
- [ ] Add `debug=true` support for deeper error traces
- [ ] Add friendly prompts like “Ready to log this?”

---

> Latest: Core tools refactored. Now targeting incident logging, SQL schema sync, and downstream tool readiness.

> Managed by QAPod — scope owned, batch-controlled.