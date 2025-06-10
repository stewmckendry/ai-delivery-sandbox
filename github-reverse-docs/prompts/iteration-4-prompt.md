## Iteration 4: Deep Research Prompt — Reverse Engineering GovDoc Copilot

You are a Deep Research agent with GitHub access enabled. Your task is to **reverse-engineer the current implementation of GovDoc Copilot** from the GitHub repository `ai-delivery-sandbox`, branch `sandbox-curious-falcon`. This application helps government teams generate policy and investment documents end-to-end using AI.

---

### 🔍 Primary Objective
Map the **active implementation** of GovDoc Copilot to the **user flow** it enables, identifying the logic and tooling behind each step.

---

### 📘 Context: GovDoc Copilot User Flow
GovDoc Copilot enables end-to-end document generation through structured conversations. Users can:
- Kick off with project and gate details
- Upload background and stakeholder content
- Align with Government of Canada strategies and policies
- Conduct open web research and record findings
- Generate and refine each section
- Finalize and store documents

Refer to [`policygpt_user_flow.md`](https://github.com/stewmckendry/ai-delivery-sandbox/blob/sandbox-curious-falcon/policygpt_user_flow.md) for full breakdown.

---

### 📎 Runtime Usage Signal
The following files are attached to support the research:
- `log_tool_usage.json`: end-to-end usage trace with tool calls and metadata
- `tool_catalog.yaml`: maps GPT-exposed tool names to internal modules
- `policygpt_user_flow.md`: defines the intended user flow and expected tool usage

Use these to:
- Identify the most-used toolchains and tools
- Prioritize relevant chains and filter legacy

---

### 📂 Source of Truth
For resolving implementation, trust the following:
- `tool_catalog.yaml` maps GPT-facing tool names to code paths (e.g., `app/tools/tool_wrappers/...`, `app/engines/toolchains/...`)
- `openapi.json` defines callable endpoints
- Core orchestrators: `planner_orchestrator.py`, `tool_registry.py`
- Chain registry inferred from runtime usage and orchestrators

---

### 📌 Focus Areas
Please prioritize the following capabilities:
1. **Prompt ingestion and memory system** (Redis, vector DB, PromptLog)
2. **Reference document alignment** (via `alignWithReferenceDocuments` and embedding flow)
3. **Web research and citation logging** (`webSearch`, `record_research`, `goc_alignment_search`)
4. **Section generation + revision workflows** (`generate_section_chain`, `revise_section_chain`)
5. **Toolchain orchestration** (Planner, registry, inference patterns)
6. **Final artifact assembly and formatting**

---

### 🧠 Output Expectations
1. **Definition of Ready User Stories** —
   - One per feature or capability, following: *As a [user], I want to [action], so that [goal].*
   - Include acceptance criteria if inferable from tests or behavior.

2. **Design Artifacts** —
   - **Technical Design**: module and function map, class hierarchy, orchestration notes
   - **Interface Design**: sequence of tool invocations, API routes, parameters and payload formats
   - **Data Design**: data models, Redis/vector stores used, schemas or structures where available

3. **Test Outlines** —
   - Derived from test cases or traceable behavior (e.g., `test_*.py`)
   - Should reflect system-level integration expectations

4. **Modernization Opportunities** —
   - Gaps in implementation vs. intent
   - Potential upgrades to architecture, tooling, or user interaction flow

---

### 🧩 Prompt Enhancements
- You may assume prompt templates live in `app/prompts/`
- Ignore `scripts/`, `redis/`, and `docs/` unless called explicitly
- Legacy `memory_` tools should be deprioritized unless found in usage log
- YAML-based chains may exist — derive from runtime usage if unclear

---

### 📄 Output Format
Please provide a well-structured Markdown report with:
- One section per capability (as defined in Focus Areas)
- Each section should include: relevant user stories, design elements, test outline, and gaps/opportunities
- Code paths and filenames cited inline (e.g., `app/engines/toolchains/...`)

---

### ⚠️ Limitations Acknowledged
We understand that static analysis may miss dynamic orchestration or runtime state. Please document any ambiguity and include recommendations.

---

Thank you! This PoC explores how ChatGPT + GitHub connectors can reverse-engineer legacy systems for modernization. Your results will inform real-world migration and documentation efforts.