## Iteration 6: Deep Research Prompt — Reverse Engineering GovDoc Copilot (Final Run)

You are a Deep Research agent with GitHub access enabled. Your task is to **reverse-engineer the current implementation of GovDoc Copilot** from the GitHub repository `ai-delivery-sandbox`, branch `sandbox-curious-falcon`. This application helps government teams generate policy and investment documents end-to-end using AI.

This final run builds on all previous iterations, integrating precise step-by-step user workflow logic and runtime references to eliminate ambiguity.

---

### 🔍 Primary Objective
Map the **active implementation** of GovDoc Copilot to the **real user flow** described below, identifying logic, tools, and orchestration. Provide **detailed system documentation** aligned to the user experience.

---

### 📘 Context: GovDoc Copilot Real User Flow
GovDoc Copilot enables end-to-end document generation using a structured, interactive workflow:

1. **Kick Off: Gate Setup**
   - Ask for project and gate
   - ➤ `getArtifactRequirements` → returns `session_id`, artifact list

2. **Input Upload**
   - User uploads notes, mandates, text, URLs, or files
   - ➤ `uploadProjectInputs` → logs + summarizes inputs

3. **Reference Alignment**
   - ➤ `listReferenceDocuments` → view references
   - ➤ `uploadReferenceDocument` → index new ones
   - ➤ `alignWithReferenceDocuments` → extract key content

4. **Research Context** *(Optional)*
   - ➤ Use browsing + `record_research` to store findings

5. **Input Review**
   - ➤ `reviewInputSnapshot` → digested inputs summary

6. **Section Drafting + Review**
   - ➤ `generateSectionDraft` → creates draft
   - ➤ `section_review_feedback` → revise or finalize
   - Repeat until all sections are approved

7. **Finalize Artifact**
   - ➤ `finalizeArtifact` → merges + stores complete document

➡️ See: [`project/build/wps/WP27b/policygpt_custom_gpt_guide.md`](https://github.com/stewmckendry/ai-delivery-sandbox/blob/sandbox-curious-falcon/project/build/wps/WP27b/policygpt_custom_gpt_guide.md) for flow reference.

Use `.py` and `.yaml` files as authoritative. `.md` files are contextual only.

---

### 📎 Runtime Usage Signals Provided
Attached:
- `log_tool_usage.json`: Actual tool call log across an E2E flow
- `tool_catalog.yaml`: Maps tool names to internal modules (file paths)
- `policygpt_custom_gpt_guide.md`: Human-readable flow reference

Use these to:
- Confirm active tools, toolchains, and order of execution
- Map tool logic using `module` → filepath (e.g. `app/tools/tool_wrappers/x.py`)

---

### 📂 Trust Sources
- `tool_catalog.yaml` — authoritative tool inventory and module mapping
- `openapi.json` — callable interface schema
- `planner_orchestrator.py`, `tool_registry.py` — logic registry and planner
- `app/prompts/` — prompt templates used by tools

Ignore: `scripts/`, legacy `redis/`, or unreferenced `memory_*.py`

---

### 🎯 Focus Areas
Focus your analysis on these workflows and capabilities:
- **Prompt ingestion + memory logic**
- **Embedding + alignment** with references
- **Web search + research memory**
- **Section drafting + revision chains**
- **Toolchain execution** (Planner + registry)
- **Final artifact generation** (Drive export)

---

### 🧠 Output Format
For each feature group:
1. **User Stories at DoR**
   - *As a [user], I want to [action], so that [value]*
   - Include: preconditions, dependencies, I/O, acceptance criteria

2. **Design Details**
   - **Technical**: classes, chains, orchestration
   - **Interface**: API schema, inputs, outputs
   - **Data**: redis, vector stores, embeddings, schemas

3. **Test Outline**
   - Logic validation, edge cases, mock data use

4. **Modernization Suggestions**
   - Tech debt, refactor areas, optimizations

---

### 🔁 Apply Past Lessons
Address prior issues:
- Confirm filepaths using `module` in `tool_catalog.yaml`
- Ignore `.md` and legacy files unless referenced
- Eliminate incorrect tool matches (based on actual usage)
- Validate presence of tool logic (not just existence)
- Track skipped files with reasons

---

### 📄 Deliverable Format
- Markdown preferred
- Structure output by feature focus area
- Include inline file references

Thank you! This round should set a benchmark for reverse-engineering legacy systems using GitHub + ChatGPT Deep Research.