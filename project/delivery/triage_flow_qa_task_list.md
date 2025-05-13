# 🧠 Triage Flow QA – Fix Task List

This task list addresses key issues surfaced during full triage testing via ConcussionGPT. Issues include flow/UX gaps, tool interface bugs, and structural schema weaknesses.

---

## ✅ Phase 1: Tool Interface Fixes

### 🔧 General
- [ ] Improve error messaging across all tools (replace `UnrecognizedKwargsError` with readable errors)
- [ ] Revalidate OpenAPI schemas to match tool expectations

### 🛠 Tool-Specific Fixes
- [ ] `assess_concussion`: Confirm expected inputs; reject extras clearly
- [ ] `log_symptoms`: Accept structured symptom list + timestamp
- [ ] `get_stage_guidance`: Clarify what `tracker_state` means and whether tool needs rework

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

Once complete, these changes will improve data consistency, user understanding, and system resilience.

> Created by QAPod, based on triage-to-log incident test retro.