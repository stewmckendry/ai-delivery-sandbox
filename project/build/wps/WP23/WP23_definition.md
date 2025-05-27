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