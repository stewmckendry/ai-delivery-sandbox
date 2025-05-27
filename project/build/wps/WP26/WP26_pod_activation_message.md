### 📦 Work Package Activation

**To:** `WP26Pod`

**From:** Lead Pod (via Human Lead)

**Subject:** Activate `WP26 – Composable Planner`

---

### 🔍 Context
We’re enabling a flexible, user-configurable planner tool that lets GPT or a UI define which tools to use in what order when generating a document.

This makes the planning step fully configurable and helps downstream GPTs use tailored sequences for different artifact types, levels of review, or planner personas.

---

### 🗿 Instructions
1. Review your WP scope and deliverables (see: `WP26_definition.md`)
2. Fetch tool metadata using `tool_registry_builder` (schema, inputs, description)
3. Draft YAML plan templates for 2-3 sample artifacts (Funding Memo, Risk Plan)
4. Implement `composable_planner.py` with functions to:
   - Load + validate YAML plan
   - Resolve tools from registry
   - Execute toolchain and log outputs
5. Log all steps using PromptLog and ReasoningTrace
6. Build tests for malformed plans, tool errors, and trace validation

---

### 📂 Repo Info
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Folder:** `project/build/wps/WP26/`
- **Task ID:** `2.2_build_and_patch`

---

### 🧪 Example Test: Funding Memo
Inputs:
- Memory: Project summary
- Config: YAML steps: memory_retrieve → generate_section_chain → refine → validate → commit

Output:
- Artifact committed with trace
- Planner steps recorded to PromptLog

---

Let’s make planning composable 💡