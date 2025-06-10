
# 🧠 Reverse Engineering Summary: GovDoc Copilot - Business Case Drafting Flow

## 🔍 Chain of Thought (Research Strategy & Steps)

The objective was to reverse-engineer the `ai-delivery-sandbox` repository on branch `sandbox-curious-falcon`, focusing on the **Business Case drafting** flow. The following strategy guided the research:

1. **Anchor on Key Entry Points**: Started with `main.py`, `openapi.json`, and `api_router.py` to understand exposed API endpoints and their associated inputs/outputs.
2. **Trace Through Orchestration Layers**: Followed request flow through `planner_orchestrator.py` and `tool_registry.py`, identifying how intents (like `generate_section`) map to toolchains.
3. **Decompose Toolchains**: Fully reviewed `IngestInputChain`, `GenerateSectionChain`, and `AssembleArtifactChain` for their steps, sub-tools, prompt usage, and persistence logic.
4. **Analyze Prompts and LLM Tooling**: Studied how prompts are templated (via Jinja2/YAML) and injected into OpenAI GPT-4 through `llm_helpers` and `tool_wrappers`.
5. **Validate via WP Test Files**: Used WP7 and WP24 test runner scripts as informal end-to-end test documentation and validation of inferred behavior.
6. **Focused Only on Active Paths**: Skipped legacy/script/framework code as instructed unless explicitly linked.

---

## 📊 File Review Summary

| Review Status   | File Type              | Count | Notes |
|-----------------|------------------------|-------|-------|
| ✅ Fully Reviewed | `toolchains/*.py`       | 4     | Includes `IngestInputChain`, `GenerateSectionChain`, `AssembleArtifactChain`, `GenerateFullArtifactChain` |
| ✅ Fully Reviewed | `tool_wrappers/*.py`    | 5     | Includes `QueryPromptGenerator`, `SectionSynthesizer`, `SectionRefiner`, `uploadTextInput`, etc. |
| ✅ Fully Reviewed | `llm_helpers.py`        | 1     | Central for prompt templating and GPT calls |
| ✅ Fully Reviewed | `planner_orchestrator.py` | 1     | Maps high-level intent to chains |
| ✅ Fully Reviewed | `tool_registry.py`      | 1     | Tool name → class mapping |
| ✅ Fully Reviewed | `project_profile_engine.py` | 1  | For profile persistence and retrieval |
| ✅ Fully Reviewed | `prompts/generate_section_prompts.yaml` | 1 | YAML prompt template used in section generation |
| ✅ Fully Reviewed | `test/WP7/test_runner.py` and `test/WP24/test_runner.py` | 2 | Validated flow execution |
| 🔍 Skimmed       | `memory_sync.py`        | 1     | Only parts for `log_tool_usage` used in chains |
| 🔍 Skimmed       | `gate_reference_v2.yaml`| 1     | Used to identify section order and artifacts |
| ❌ Skipped       | `framework/`            | ~10+  | Marked as out of scope; not referenced in active flow |
| ❌ Skipped       | `scripts/`              | ~5    | Not referenced by planner, tools, or chains |
| ❌ Skipped       | `docs/`                 | ~10   | Treated as passive reference, not source of behavior |
| ❌ Skipped       | `legacy/`               | ~5    | Deprecated; no active chain or planner calls |

---

## ⚠️ Challenges Encountered

1. **Ambiguity in Tool Invocation**  
   - Tools were invoked dynamically by name through the registry, making it hard to trace exact flow without running the system.
   - Helped by checking test scripts and reviewing each tool class manually.

2. **Prompt Loading via HTTP**  
   - Prompts were loaded via GitHub raw URL fetches at runtime, which obscured their contents unless traced through `llm_helpers`.
   - Reading `generate_section_prompts.yaml` directly was essential to understand expected LLM behavior.

3. **Orchestrator vs. Toolchain Duplication**  
   - Some tasks (e.g. `generate_section`) were handled both in `PlannerOrchestrator` and a `GenerateSectionChain` class. Required cross-checking for canonical implementation.

4. **Implicit Data Contracts**  
   - Inputs/outputs between tools and chains were Python dicts with loosely defined schemas, making static understanding harder without relying on test runs or examples.

5. **Limited API Documentation**  
   - The `openapi.json` file was incomplete or absent; most understanding of schema came from test scripts and reverse inference from parameter usage in chains.

---

## 🙏 What Would Have Helped

- Clear indication of which planner → chain → tool flows were canonical and maintained (vs legacy/deprecated).
- A high-level map (visual or YAML) showing valid planner intents and the corresponding toolchains.
- Explicit example payloads or saved inputs/outputs from real usage runs.
- OpenAPI spec with schema definitions for inputs/outputs to verify assumptions on field names and formats.

---

