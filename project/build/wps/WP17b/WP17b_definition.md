## WP17b – Section Draft Generation from Inputs

### 🎯 Objective
Extend the capabilities of PolicyGPT to generate structured draft content for each section of an artifact using user-provided inputs and embedded reference documents.

### 📦 Scope of Work
**In Scope:**
- Use PromptLog and memory embeddings to ground generation
- Generate YAML or markdown for individual sections
- Validate against intent and acceptance criteria
- Wire into planner and confirm-to-draft UX
- Build `composeSectionDraft` tool

**Out of Scope:**
- Full artifact assembly (handled in WP18)
- Post-generation feedback (handled by WP1a)

### 🚀 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/tools/tool_wrappers/composeSectionDraft.py` | Drafts a single section using context and inputs |
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