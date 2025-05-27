# WP23 Definition – Artifact Refinement from Feedback

## 🧠 Summary
Design and implement a feedback-driven toolchain that updates existing artifact sections using new inputs, comments, or user feedback.

## 🎯 Objective
Build a `revise_section_chain` toolchain that:
- Accepts feedback or updates (from comments, Slack, edited text)
- Identifies relevant section(s)
- Rewrites and logs changes with full trace
- Validates and re-commits updated content

---

## 🧱 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/engines/toolchains/revise_section_chain.py` | Orchestrates feedback ingestion → section revision |
| `app/tools/tool_wrappers/feedback_mapper.py` | Maps input to section(s) and identifies change types |
| `app/tools/tool_wrappers/section_rewriter.py` | Regenerates section with updated context |
| `app/tools/tool_wrappers/feedback_preprocessor.py` | Optional cleaner/normalizer for noisy input comments |
| `project/prompts/revision_prompts.yaml` | Prompt templates for edit types |
| `project/test/wps/WP23/test_revise_section_chain.py` | Test plan for E2E refinement flow |
| `project/build/wps/WP23/WP23_toolchain_plan.md` | Design + integration notes |
| `app/tools/tool_wrappers/manualEditSync.py` | Detect, parse, and sync user-submitted text |
| `project/prompts/edit_trace_templates.yaml` | Prompts to describe manual or verbatim edit intent |
| `project/build/wps/WP23/WP23_edit_modes.md` | Mode reference: GPT revise vs user edit vs upload |

---

## 🧭 User Journey Pathways for WP23 Toolchain

This toolchain will support artifact refinement through multiple entry points:

| Scenario | Trigger Source | Description |
|---------|----------------|-------------|
| Draft edits post-generation | `generate_section_chain` output | User or GPT requests improvements to initial draft |
| New input upload | `uploadTextInput`, `uploadFileInput`, `uploadLinkInput` | Adds new context to an existing artifact section |
| Stakeholder feedback | Manual or external comment ingestion | Revisions triggered from shared Google Doc, email, or Slack |
| New research result | Tool calls to `web_search`, `goc_alignment_search` | Updates needed after external validation or discovery |
| Corpus expansion | `queryCorpus` or re-indexing | Refine section based on newly loaded evidence base |

---

---

## 🔁 Post-Revision Handling Scenarios

After a section is revised, downstream workflows vary based on how and where the edits occurred.

### Scenario A: Revise + Re-Assemble Full Artifact

| Trigger | Action |
|--------|--------|
| One or more sections revised | Run `assemble_artifact_chain` to merge updated sections |
| Outcome | Creates new version in `DocumentVersionLog`, exports to Drive |

### Scenario B: GPT-In-Chat Section Edits (Verbatim Save)

| Trigger | User and GPT co-edit section in chat |
| Action | GPT directly writes final user-reviewed content to `ArtifactSection.text` |
| Trace | Logs prompt summary and decision path in `ReasoningTrace` |
| Optional | User may annotate reason or source of change via `AuditTrail` or `PromptLog` metadata |

### Scenario C: Manual Edit + Upload

| Trigger | User updates Google Doc, re-uploads or pastes |
| Action | GPT detects change (e.g., via comparison or direct mapping) |
| Options | 
  - Update `ArtifactSection.text` verbatim
  - Archive previous version
  - Optionally re-run `validateSection` tool |
| Provenance | Log edit origin as “manual” in `generated_by`, tag update source in `ReasoningTrace` |
| Drive Sync | New Drive URL committed to `DocumentVersionLog.google_doc_url` if replaced


---


## 🗃️ Database Tables: Read/Write Scope for WP23

| Table | Read/Write | Usage |
|-------|------------|-------|
| `ArtifactSection` | Read/Write | Fetch current draft, update with new content |
| `PromptLog` | Read/Write | Log new revision prompt/input/output |
| `ReasoningTrace` | Read/Write | Append steps explaining revision logic |
| `AuditTrail` | Write | Track revision trigger and execution |
| `DocumentFeedback` | Optional Write | If feedback came from stakeholder |
| `ProjectProfile` | Read | Align section scope with current gate |

No schema changes required. Reuse `status`, `version`, and `sources` columns in `ArtifactSection`. Reuse `steps` and `draft_chunks` in `ReasoningTrace`.

---

## ⚙️ Technical Design Notes

- **Inputs**:
  - Freeform text comment (Slack, chat)
  - Revised section draft (edited directly)
  - Uploaded document/file
  - Auto-detected delta (from corpus/research)

- **Modules**:
  - `feedback_mapper.py`: Determine which section(s) are impacted
  - `section_rewriter.py`: Run updated synthesis using LLM
  - `revision_prompts.yaml`: Load correct prompt template based on revision type

- **Flows**:
  1. Normalize and summarize feedback
  2. Map feedback to one or more `ArtifactSection`
  3. Load prior `PromptLog`, `ReasoningTrace` as grounding
  4. Regenerate content and validate
  5. Write new entries, version tag, and trace

---

## ✅ Task Breakdown

| Task | Owner | File(s) |
|------|-------|---------|
| Design toolchain interface | WP23 | `revise_section_chain.py` |
| Map feedback to section | WP23 | `feedback_mapper.py` |
| Prompt and rerun LLM | WP23 | `section_rewriter.py`, `revision_prompts.yaml` |
| Update DB | WP23 | `ArtifactSection`, `PromptLog`, `ReasoningTrace` |
| Write test cases | WP23 | `test_revise_section_chain.py` |
| Plan logging trace structure | WP23 | Extend `ReasoningTrace.steps` |

---

## 🔁 Toolchain Integration
- Used in Journey B (Refining Artifacts)
- Optionally triggered from GPT when new input/comment is detected
- Reuses ReasoningTrace + PromptLog to track diffs
- Ensures provenance logging for each revision

---

## 🧪 Testing
| File Path | Description |
|-----------|-------------|
| `project/test/wps/WP23/test_revise_section_chain.py` | Tests: mapping, revision quality, diff trace, DB commits |

---

## 🔮 Future Extensions
- Suggest diffs inline (à la Git redline)
- Annotate sections with “last updated from” comment source
- Support redline generation for stakeholder review
- Add comment-level classification (e.g., tone vs fact vs structure)