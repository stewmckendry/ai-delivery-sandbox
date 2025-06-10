📁 **Repository**: `ai-delivery-sandbox`
🌿 **Branch**: `sandbox-curious-falcon`
🎯 **Objective**: Reverse-engineer this repo to extract artifacts that support system understanding, migration, and potential reimplementation.

---

## 🧭 Background Context (From CoachingTheMachine Blog)
> GovDoc Copilot is a GPT-powered assistant designed for the Government of Canada's Project Management Framework (PMF). It helps draft complex project documents like Business Cases, Charters, and Transition Plans — step-by-step — while ensuring alignment with GoC gating requirements, Treasury Board policies, and mandate letters.
>
> In a typical session, the user selects a document type (e.g. Gate 0 Investment Proposal), uploads internal notes, and asks the Copilot to perform research, extract policy alignments, and draft content in structured sections. The AI integrates references, remembers context, adapts tone, and produces near-final artifacts with built-in QA and iterative feedback support.

---

## 🔄 Iteration 2 Refinements

### ⚠️ Repo Characteristics
- Inconsistent organization; includes both active and outdated files.
- Dead code, copied components, or irrelevant references may exist.

### ✅ Strategy
Please:
1. **Start with the OpenAPI schema or `main.py`** to identify available tools/routes.
2. **Traverse the system top-down** from API interfaces to handler logic to helper modules.
3. **Prioritize active code paths** (recently modified, integrated, or referenced by chain/tool logic).
4. **Use markdowns and outdated scripts for context only** — avoid inferring functionality from them.

### 🔍 Focus Areas to Include
- **Embedding + vector DB functionality** (e.g., reference document search, alignment)
- **Web research and citation tracking logic**
- **Prompt construction + memory handoff patterns**

---

## 📤 Expected Outputs

### 1. 🧾 User Stories @ Definition of Ready
- Use format: *As a [user], I want [function] so that [benefit]*
- Include: Acceptance criteria, assumptions, dependencies

### 2. 🛠️ Design Decomposition
- **Technical:** modules, chains, tools, external libraries
- **Interface:** APIs, FastAPI routes, UI paths
- **Data:** object schema, embedding flow, data transformations

### 3. ✅ Test Suite Outline
- System test scenarios (black box)
- Component tests
- Data validation

### 4. 🧭 Modernization Opportunities
- Refactoring, modularization, separation of concerns

📝 **Output Format:**
Return structured markdown with clear sections and subheadings.

### 💡 Optional
If the repo is too large to analyze in one pass, suggest a chunked approach (e.g., by folder or tool group).