📁 **Repository**: `ai-delivery-sandbox`
🌿 **Branch**: `sandbox-curious-falcon`
🎯 **Objective**: Reverse-engineer this repo to extract artifacts that support system understanding, migration, and potential reimplementation.

---

## 🧭 Background Context (GovDoc Copilot)
> GovDoc Copilot is a GPT assistant built for the Government of Canada’s PMF. It helps teams draft compliant artifacts like Business Cases and Charters by guiding users through reference ingestion, policy alignment, and structured co-drafting. Artifacts are generated from user prompts, enriched with web research and internal notes.

---

## 🔄 Iteration 3 Refinements

### ✅ Strategy
1. **Begin with `openapi.json` and `main.py`** to identify user-facing tools and endpoints.
2. **Traverse from routes → chains → tools** to map functionality.
3. **Prioritize recently modified, clearly linked code**.
4. **Use `api_router.py`, `tool_registry.py`, and `planner_orchestrator.py` as primary maps.**
5. **Treat README/docs/scripts/redis/framework folders as context only. Do not infer behavior from them unless linked.**

### ⚠️ Exclude by Default
Unless explicitly referenced in active flows:
- `framework/`
- `redis/`
- `scripts/`
- `legacy/`
- `docs/`

### 📁 Key Folders to Prioritize
- `toolchains/`
- `tool_wrappers/`
- `prompts/`
- `db/`

### 📄 Key Files to Anchor From
- `main.py`
- `openapi.json`
- `api_router.py`
- `tool_registry.py`
- `planner_orchestrator.py`
- `memory_sync.py`
- `tool_catalog.yaml`
- `gate_reference_v2.yaml`

### 🔍 Functional Areas to Include (not exhaustive)
If present and active, please include:
- **Embedding + vector DB search**
- **Web research and citation tracking**
- **Prompt construction + memory handoffs**

---

## 📤 Expected Outputs

### 1. 🧾 User Stories @ Definition of Ready
- Format: *As a [user], I want [function] so that [benefit]*
- Include: Acceptance criteria, assumptions, dependencies

### 2. 🛠️ Design Decomposition
- **Technical:** modules, chains, tools, libraries
- **Interface:** FastAPI endpoints, schema
- **Data:** schema, flows, embedding logic

### 3. ✅ Test Suite Outline
- Functional test cases
- Component boundaries
- Input validation and edge cases

### 4. 🧭 Modernization Opportunities
- Identify duplication, tight coupling, or untracked assumptions

📝 **Format**: Markdown sections with bullets, tables, or diagrams where helpful.