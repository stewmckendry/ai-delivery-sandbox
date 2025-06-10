
# 📚 Reverse Engineering Research Summary: `ai-delivery-sandbox` (`sandbox-curious-falcon`)

## 🧠 Chain of Thought & Research Strategy

To reverse-engineer the `ai-delivery-sandbox` repository and extract artifacts useful for system understanding, migration, and reimplementation, I followed this top-down approach:

1. **Starting Point:** Began with `main.py`, `api_router.py`, and `openapi.json` to identify available routes, API structure, and entry points to the app.
2. **Tool & Chain Analysis:** Traced route handlers to the `PlannerOrchestrator`, then into prioritized toolchains (`toolchains/`) and their associated tool wrappers (`tool_wrappers/`), confirming the orchestration logic and atomic tool behavior.
3. **Prompt Usage:** Examined `prompts/` folder for examples of externalized LLM logic (YAML-based prompts), their loading mechanism, and dynamic rendering behavior.
4. **Data & Storage:** Analyzed `db/` (SQLAlchemy models and DB logic) and `redis/` (assumed future intent of caching/session handling) for system persistence and memory design.
5. **Cross-reference:** Verified usage patterns and assumptions using work package notes and in-code docstrings, confirming design intents and mismatches.

All findings were synthesized into four outputs: User Stories, Design Decomposition, Test Suite Outline, and Modernization Opportunities.

---

## 📊 File Analysis Summary

| Category       | Fully Reviewed | Skimmed | Skipped | Notes |
|----------------|----------------|---------|---------|-------|
| `main.py`      | ✅ 1            | –       | –       | Entry point |
| `api_router.py`| ✅ 1            | –       | –       | API wiring |
| `openapi.json` | ✅ 1            | –       | –       | Contract for API |
| `tool_registry.py` | ✅ 1        | –       | –       | Tool loading |
| `planner_orchestrator.py` | ✅ 1 | –       | –       | Intent-based chain routing |
| `memory_sync.py` | ✅ 1         | –       | –       | Logging / trace saving |
| `tool_catalog.yaml` | ✅ 1      | –       | –       | Tool declarations (planned use) |
| `gate_reference_v2.yaml` | ✅ 1 | –       | –       | Artifact/gate schema |
| `toolchains/` (7 files) | ✅ 6 | 1       | 0       | Core: IngestInputChain, GenerateSectionChain, AssembleArtifactChain |
| `tool_wrappers/` (12 files) | ✅ 9 | 2 | 1       | Skipped: legacy or deprecated wrappers |
| `prompts/` (4 YAMLs) | ✅ 4     | –       | –       | Prompt schema & templates |
| `db/` (5 model files) | ✅ 5    | –       | –       | SQLAlchemy models |
| `redis/` (3 files) | 0         | 1       | 2       | Minimal integration or usage |
| `test/` (2 test harnesses) | ✅ 2 | –   | –       | Confirmed planner & tool test support |
| `docs/`, `scripts/`, legacy roots | 0 | 3 | 5 | Outdated or markdown only context |

---

## 🚧 Research Challenges & Suggestions

### Challenges Faced
- **Mixed Code States:** Many files were in partial or deprecated states (e.g., early Redis stubs, non-functional wrappers), which required active filtering to avoid misleading assumptions.
- **Manual Mapping of Chains:** The lack of an explicit toolchain registry (only implicit in PlannerOrchestrator) made it time-consuming to identify all valid toolchains and their tool sequences.
- **Prompt Templates as GitHub Links:** Dynamic loading of prompts via raw GitHub URLs made static analysis brittle. Some required assumptions on what the prompt text would contain.
- **Sparse Inline Docs:** While some docstrings existed, most orchestration logic and API endpoint rationale had to be inferred from code flow or test artifacts.

### Prompt Additions That Would Have Helped
- A list of *active vs deprecated chains/tools* from recent usage
- An explicit prompt to ignore legacy `scripts/`, `docs/`, and early `redis/` prototypes unless directly referenced
- A note on whether prompt templates should be resolved via GitHub links or assumed present locally (for validation)
- Clear guidance on whether ReasoningTrace was YAML-based or DB-persisted for analysis

---

✅ **Next Steps Suggested:** Maintain a toolchain index, refactor Planner to declaratively register toolchains, and streamline prompt template access to avoid dynamic fetches from external URLs during execution or inspection.
