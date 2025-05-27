# WP24 Task List – Autopilot: Full Artifact Generator

## 📌 Core Implementation Tasks

| Task ID | Description | Owner | Status |
|---------|-------------|--------|--------|
| T1 | Draft design plan (WP24_toolchain_plan.md) | WP24Pod | ✅ Done |
| T2 | Implement `generate_full_artifact_chain.py` | WP24Pod | ⏳ In Progress |
| T3 | Implement `refine_document_chain.py` | WP24Pod | ⬜ Not Started |
| T4 | Add `TaskMetadata.py` model | WP24Pod | ⬜ Not Started |
| T5 | Write `task_metadata.sql` (SQL table create) | WP24Pod | ⬜ Not Started |
| T6 | Write `test_generate_full_artifact.py` | WP24Pod | ⬜ Not Started |
| T7 | Refactor `section_synthesizer.py` to use `llm_helpers.py` + central prompts | WP24Pod | ⬜ Not Started |
| T8 | Refactor `section_refiner.py` similarly | WP24Pod | ⬜ Not Started |
| T9 | Add entries to `tool_catalog.yaml` + `gpt_tools_manifest.json` | WP24Pod | ⬜ Not Started |
| T10 | Build summarizer for section context carryover | WP24Pod | ⬜ Not Started |
| T11 | Add safeguards for token limit pre-checking | WP24Pod | ⬜ Not Started |
| T12 | Move `plan_sections` and `summarize_previous` into `section_helpers.py` | WP24Pod | ⏳ In Progress |
| T13 | Refactor `generate_section_chain` to accept and log `context_summary` | WP24Pod | ⏳ In Progress |
| T14 | Refactor `assemble_artifact_chain` to include `refine_document_chain` step | WP24Pod | ⬜ Not Started |
| T15 | Create and use shared `get_token_count` utility | WP24Pod | ⬜ Not Started |
| T16 | Refactor `generate_section_chain` and `assemble_artifact_chain` to use `llm_helpers.py` + prompt templates | WP24Pod | ⬜ Not Started |

## 🔄 Review & Feedback Tasks

| Task ID | Description | Reviewer | Status |
|---------|-------------|----------|--------|
| R1 | Human Lead review of `WP24_toolchain_plan.md` | Human Lead | ✅ Done |
| R2 | GitHub review of committed Python + SQL files | Human Lead | ⬜ Pending |
| R3 | End-to-end test run + demo | Human Lead | ⬜ Pending |

Let me know if you'd like to reprioritize or adjust task scope. I’ll proceed with implementation of T12, T13, and T14 next.