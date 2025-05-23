## WP17b – Section Draft Generation from Inputs

### 🎯 Objective
Extend the capabilities of PolicyGPT to generate structured draft content for each section of an artifact using user-provided inputs and embedded reference documents.

### 📦 Scope of Work
**In Scope:**
- Implement planner-triggered flow to convert user inputs (from `PromptLog`) and memory enbeddings into structured drafts for `ArtifactSection`.
- Leverage `compose_and_cite` and `searchKnowledgeBase` tools.
- Align to `dense_artifact_generation.md` design patch.
- Track outputs in `ReasoningTrace` and `ArtifactSection` tables.
- Wire into planner and confirm-to-draft UX

**Includes:**
- Tool: `compose_and_cite`
- Input source: PromptLog (user inputs tagged by section + intent)
- Planner logic to detect readiness and generate draft.

**Out of Scope:**
- Full artifact assembly (handled in WP18)
- Post-generation feedback (handled by WP1a)

### 🚀 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/tools/tool_wrappers/compose_and_cite.py` | Drafts a single section using context and inputs |
| `project/prompts/section_drafting_prompt.md` | LLM template for drafting a section based on intent |

### Supporting Documentation to Create

To ensure full coverage and reproducibility, WP17b should generate the following artifacts:

- **Design Plan**
  - Path: `project/build/wps/WP17b/WP17b_design_plan.md`
  - Describes tool behavior, flow from PromptLog to ArtifactSection, planner logic, and UX trigger points

- **Task List**
  - Path: `project/build/wps/WP17b/WP17b_task_list.md`
  - Checklist format with owners, estimated durations, and status for each task

- **Test Plan**
  - Path: `project/test/WP17b/WP17b_test_cases.md`
  - Defines input cases, expected outputs, and CLI or API usage steps to validate

- **Deploy Steps**
  - Path: `project/deploy/WP17b/WP17b_deploy_steps.md`
  - Describes CLI, DB model, or config setup needed to run tools

- **Tool + Prompt Docs**
  - Path: `project/build/wps/WP17b/compose_and_cite.md`
  - Describes interface, input/output schema, and example use of the tool

---

### (2) Task Breakdown

1. **Design + Planning**
   - Read WP definition and all referenced specs
   - Draft and commit the design plan
   - Write task list with deliverables, phases, and owners

2. **Implement `compose_and_cite` Tool**
   - Use PromptLog entries and planner input
   - Incorporate embedded snippets from corpus
   - Write to `ArtifactSection`, log to `ReasoningTrace`

3. **Create Section Draft Prompt**
   - Commit prompt template aligned to input tags and content goals

4. **Integrate with Planner**
   - Confirm trigger flow (confirm-to-draft)
   - Register tool in planner YAML trace

5. **Generate Test Cases**
   - Include input examples from PromptLog + corpus
   - Verify YAML or Markdown output
   - Confirm retry and partial completion support

6. **Document + Deploy**
   - Write deploy steps and tool documentation
   - Validate with Human Lead

7. **Submit Final Update**
   - Confirm outputs meet acceptance criteria
   - Link to all deliverables and status update

### ✅ Acceptance Criteria
- [ ] Tool generates structured content (YAML or markdown)
- [ ] Section content aligns with metadata intent and evidence
- [ ] Tool integrates with planner or confirm-to-draft UX
- [ ] Supports retries and partial completions

### 🔗 Dependencies
- WP16 (input capture)
- WP9 (PromptLog memory)
- WP18 (assembly after draft)

**Links:**
- DB schema: `ArtifactSection`, `ReasoningTrace`
- Design: `dense_artifact_generation.md`

### 📥 Inputs
- metadata: gate, artifact, section, intent
- user inputs from PromptLog
- optionally retrieved corpus snippets

### 📤 Outputs
- Drafted section YAML or markdown
- Evaluation log (optional)

### 🧠 Notes
- Enables modular generation of documents one section at a time
- Supports gated workflow by matching gate requirements to output