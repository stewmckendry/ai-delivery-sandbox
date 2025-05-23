# 🧪 Review: WP17b `generate_section` Toolchain vs MCP-Oriented Recommendations

## ✅ Summary
WP17b successfully implemented a modular, testable `generate_section` toolchain integrating `memory_retrieve`, `section_synthesizer`, and `section_refiner` with strong logging and DB integration. It aligns well with many of the MCP-inspired code orchestration best practices.

This review compares the implemented toolchain to the MCP report’s recommendations and identifies remaining gaps, followed by a concrete action plan.

---

## 🔍 Alignment to MCP Recommendations

| Recommendation | Status | Notes |
|----------------|--------|-------|
| Code orchestration | ✅ Done | `GenerateSectionChain` centralizes logic in code, not GPT |
| Modular tools | ✅ Done | Each tool is discrete, validated, and testable |
| DB write separation | ✅ Done | Final result and trace stored via `save_artifact_and_trace` |
| Trace logging | ✅ Done | Tool outputs stored in structured trace object |
| GPT separation | ⚠️ Partial | Planner is not invoked by GPT yet, but UI handoff pattern unclear |
| Schema validation | ❌ Missing | No explicit schema checks on tool outputs before DB write |
| Chunking / retry | ❌ Missing | Draft is single-pass, not chunked or retryable |
| Versioned contract logging | ❌ Missing | Trace logs tool steps but no schema or tool version references |

---

## ⚙️ Proposed Enhancements

### 1. Add Output Schema Checks
- Use `jsonschema` or `pydantic` to validate outputs of `section_synthesizer` and `section_refiner`
- Raise warnings or reject malformed output before writing to DB

### 2. Store Tool Versions and Schemas in Trace
- Add fields to `trace['steps']` for `tool_version` and `schema_version`
- Hardcode for now, plan for dynamic lookup later

### 3. Add Chunking Support to Synthesizer
- Modify `section_synthesizer` to support multiple chunks per draft
- Return list of chunks + combined draft
- Update ReasoningTrace to capture each chunk separately

### 4. Clarify GPT-UI Role
- Define system instruction that GPT should call planner, not generate sections
- Update `/tasks/confirm_draft_start` or UI to use structured planner intent pattern

---

## 🧩 Next Steps

| Item | Owner | Path |
|------|-------|------|
| Add `section_draft.schema.json` | WP12 | `/schemas/` |
| Patch `section_synthesizer.py` | WP17b | `/tools/tool_wrappers/` |
| Add version logging to `GenerateSectionChain` | WP17b | `/toolchains/` |
| Update ReasoningTrace writer | WP17b | `/engines/memory_sync.py` |
| GPT role clarification patch | WP16 | GPT system instructions |

---

## ✅ Verdict
WP17b delivered a high-quality foundation. With minor extensions to align with the MCP insights (validation, chunking, trace contracts), the `generate_section` toolchain will be robust, scalable, and future-ready.