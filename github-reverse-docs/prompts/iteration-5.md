## Iteration 5: Deep Research Prompt — Reverse Engineering GovDoc Copilot (Final Pass)

You are a Deep Research agent with GitHub access enabled. Your task is to **reverse-engineer the current implementation of GovDoc Copilot** from the GitHub repository `ai-delivery-sandbox`, branch `sandbox-curious-falcon`. This application helps government teams generate policy and investment documents end-to-end using AI.

This is the final and most detailed iteration. You will build upon all prior outputs to generate a high-fidelity blueprint of the system’s behavior, artifacts, and architecture.

---

### 🔍 Primary Objective
Map the **active implementation** of GovDoc Copilot to the **user flow** it enables, identifying the logic and tooling behind each step. Prioritize **granularity** in the outputs.

---

### 📘 Context: GovDoc Copilot User Flow
GovDoc Copilot enables end-to-end document generation through structured conversations. Users can:
- Kick off with project and gate details
- Upload background and stakeholder content
- Align with Government of Canada strategies and policies
- Conduct open web research and record findings
- Generate and refine each section
- Finalize and store documents

Refer to [`policygpt_user_flow.md`](https://github.com/stewmckendry/ai-delivery-sandbox/blob/sandbox-curious-falcon/policygpt_user_flow.md) for a detailed journey. Treat markdown files as context only; `.py` and `.yaml` files are authoritative.

---

### 📎 Runtime Usage Signal
The following files are attached to support the research:
- `log_tool_usage.json`: end-to-end usage trace with tool calls and metadata
- `tool_catalog.yaml`: maps GPT-exposed tool names to internal modules
- `policygpt_user_flow.md`: defines the intended user flow and expected tool usage

Use these to:
- Determine which tools and chains are actually used
- Filter out deprecated, stubbed, or unused paths
- Confirm file paths using `module` attribute (e.g., `reviseSectionDraft: module: app.tools.tool_wrappers.section_review_feedback` → `app/tools/tool_wrappers/section_review_feedback.py`)

---

### 📂 Source of Truth
Trust the following sources when determining implementation logic:
- `tool_catalog.yaml`: **authoritative inventory** of tools and toolchains, with file path mappings
- `openapi.json`: defines callable API endpoints
- Core orchestrators: `planner_orchestrator.py`, `tool_registry.py`
- Prompt templates: stored in `app/prompts/`

Ignore `scripts/`, `redis/`, and legacy `memory_*.py` unless referenced by the above.

---

### 📌 Focus Areas
Prioritize the following features for detailed analysis:
1. **Prompt ingestion + memory architecture** (PromptLog, Redis, embeddings)
2. **Reference alignment** (embedding flows + `alignWithReferenceDocuments`)
3. **Web research workflows** (`webSearch`, `record_research`, `goc_alignment_search`)
4. **Section generation & revision** (`generate_section_chain`, `revise_section_chain`, `section_synthesizer`, etc.)
5. **Toolchain orchestration logic** (Planner, registry, inference patterns)
6. **Final assembly and drive export** (`storeToDrive`, artifact finalization)

---

### 🧠 Output Expectations
1. **User Stories at Definition of Ready**
   - Format: *As a [user], I want to [action], so that [value].*
   - Include:
     - Preconditions and dependencies
     - Input/output expectations
     - Acceptance criteria (inferred from code or flow)

2. **Design Artifacts**
   - **Technical Design**: class/function architecture, orchestration flows
   - **Interface Design**: API routes, chain/tool sequences, parameter formats
   - **Data Design**: schemas, data stores, entity relationships, embeddings

3. **Test Outlines**
   - Derive from `test_*.py` or implied behaviors
   - Include edge cases, mock data strategies, and test coverage gaps

4. **Modernization Opportunities**
   - Call out tech debt, dead paths, refactor candidates
   - Suggest architecture optimizations and integration improvements

---

### 🔁 Build on Lessons Learned
Please address challenges surfaced in Iteration 4:
- Explicitly trace chain orchestration beyond naming
- Surface input/output flow logic per toolchain
- Include semantic patterns in prompt templates
- Flag areas where test coverage is absent or unclear

**Additional Notes:**
- All referenced files are accessible in the GitHub repo.
- Prefer `.py` and `.yaml` files over `.md` as implementation sources.
- When resolving toolchains, use the `tool_catalog.yaml` + orchestrators to identify tool call sequence.
- YAML prompt templates under `app/prompts` are valid unless stated otherwise.
- Use class/function + file path pairing (vs. string match) when searching.

---

### 📄 Output Format
Structure your report by capability area (see Focus Areas).
Each section should include:
- User stories (at DoR fidelity)
- Design overview (technical/interface/data)
- Test outlines
- Modernization opportunities

Embed code references inline (e.g., `app/engines/toolchains/...`).

---

### ⚠️ Limitations Acknowledged
We recognize that static analysis has blind spots. Document ambiguity and explain assumptions. You may refer to attached files for clarification.

---

Thank you! This final iteration informs real-world system modernization and sets the benchmark for reverse-engineering enterprise legacy codebases with ChatGPT + GitHub.