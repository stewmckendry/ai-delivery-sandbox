# 🧠 Triage Flow QA – Fix Task List

This task list addresses key issues surfaced during full triage testing via ConcussionGPT. Issues include flow/UX gaps, tool interface bugs, and structural schema weaknesses.

---

## ✅ Phase 1: Tool Interface Fixes

### 🔧 General
- [x] Improve error messaging across all tools (replace `UnrecognizedKwargsError` with readable errors)
- [x] Revalidate OpenAPI schemas to match tool expectations

### 🛠 Tool-Specific Fixes
- [x] `assess_concussion`: Pull symptom scores from DB, not request; restore assessment logic
- [x] `symptom_logger.py`: Rewrite to log one row per symptom with canonical ID, score, notes
- [x] `get_linked_symptoms.py`: Refactor to read row-based symptom logs
- [x] `db_reader.py`: Refactor symptom parsing logic to row model
- [x] `db_writer.py`: Deprecated (replaced by direct logging)
- [x] `export_to_sql.py`: Deprecated (Azure Studio now used for exports)
- [ ] `validator.py`: Update to scan row-based symptom entries and flag unexpected or missing canonical matches

---

## ✅ Phase 2: Triage Experience Improvements

### 🧭 Question Design
- [ ] Re-audit `triage_map.yaml` for correct `mode: probe`, `inform`, `select`, etc.
- [ ] Add support for branching via `next_qid_if_true/false` metadata

### 🧪 Validation
- [ ] Add `enum` or `pattern` to restrict `age_group`, `sport_type`, etc.
- [ ] Normalize symptom keys against `symptom_log_map.yaml`

---

## ✅ Phase 3: GPT UX Guardrails

- [ ] Add GPT instruction to confirm before calling each tool
- [ ] Add option to run in `debug=true` mode for better error traces
- [ ] Add clarifiers like “Ready to log?” before calling tools

---

> Latest: SymptomLog, export, and read tools are fully aligned. Validator is next to update.

> Created by QAPod, based on triage-to-log incident test retro.