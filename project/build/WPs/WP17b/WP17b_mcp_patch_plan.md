# 🔧 WP17b MCP Alignment Plan – Enhancing `generate_section` Toolchain

## 🔍 Purpose
This plan responds to WP12's MCP review and recommendations. It validates suggestions, commits to enhancements, and outlines concrete deliverables.

---

## ✅ Review Summary

| Recommendation | Response | Next Step |
|----------------|----------|-----------|
| Output schema validation | ✅ Agree | Add Pydantic schema for synthesizer/refiner outputs |
| Versioned logging | ✅ Agree | Add `tool_version` and `schema_version` to `ReasoningTrace.steps` |
| Chunking | ✅ Agree | Update `section_synthesizer` to chunk input/output and log as `draft_chunks` |
| GPT role delegation | ✅ Agree (WP16 domain) | Will interface with WP16 for Planner trigger pattern |

---

## 🔨 Deliverables

### 1. **Schema Validation**
- Create `section_draft_output.py` Pydantic model
- Validate output from `section_synthesizer`, `section_refiner`

### 2. **Trace Version Logging**
- Update `GenerateSectionChain` trace logs with `tool_version`, `schema_version`

### 3. **Chunking Support**
- Refactor `section_synthesizer` to return:
  - `raw_draft` (full text)
  - `draft_chunks`: list of strings
- Patch `save_artifact_and_trace` to save `draft_chunks`

### 4. **Support WP16 GPT Delegation**
- Confirm planner signature for GPT call
- Align input pattern with `intent`-based invocation

---

## ✅ Task List

- [ ] Add `section_draft_output.py` schema file
- [ ] Patch `section_synthesizer.py` for chunking + schema validation
- [ ] Patch `section_refiner.py` for schema validation
- [ ] Update `memory_sync.py` to log `draft_chunks`
- [ ] Patch `generate_section_chain.py` to add version tags
- [ ] Provide planner signature + sample call to WP16

---

## 🤝 Coordination
- Coordinate with WP12 on schema location + field standard
- Notify WP16 once planner is GPT-callable
- Commit all patches to `sandbox-curious-falcon` under WP17b scope