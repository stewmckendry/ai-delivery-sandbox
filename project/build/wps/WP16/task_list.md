## WP16 – Input Prompt UX Layer: Task List (Updated)

### ✅ Confirmed Scope Tasks

| ID | Task | Description | Output |
|----|------|-------------|--------|
| T1 | Prompt Schema Design | Design JSON schema for prompts + metadata | `prompt_schema.json` |
| T2 | Tool: inputPromptGenerator | Generates prompts based on gate metadata | `inputPromptGenerator.py` |
| T3 | Tool: inputChecker | Validates required input completeness | `inputChecker.py` |
| T4 | Tool Integration | Register tools in registry + manifest | `tool_registry.py`, `tool_catalog.yaml` |
| T5 | UX Flow Logic | Implements guided prompt or data dump mode | `input_prompt_flow.py` |
| T6 | PromptLog Metadata Integration | Add metadata capture to WP16 tools | Inline via `log_tool_usage()` |
| T7 | Test Package | CLI-based or config test for end-to-end | `input_prompt_test.py` |

### 🧠 References
- `gate_reference_v2.yaml`
- `triage_map.yaml`
- `tool_catalog_v3.md`
- `session_memory_model_v2.md`
- `uploadTextInput.py` / PromptLog usage pattern

---