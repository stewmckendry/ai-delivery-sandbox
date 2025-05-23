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