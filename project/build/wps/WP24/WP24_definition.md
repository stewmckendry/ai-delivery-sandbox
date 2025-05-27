# WP24 Definition – Autopilot: Full Artifact Generator

## 🧠 Summary
Design and implement a planner-driven toolchain that automates the full generation of a gate artifact from project inputs.

## 🎯 Objective
Build a `generate_full_artifact_chain` toolchain that:
- Enumerates sections from gate template
- Synthesizes each section using `generate_section_chain`
- Summarizes and commits ReasoningTrace for transparency
- Assembles and commits full document draft

---

## 🧱 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/engines/toolchains/generate_full_artifact_chain.py` | Main orchestration toolchain |
| `project/prompts/full_artifact_generation.yaml` | Planner prompt logic |
| `project/build/wps/WP24/WP24_toolchain_plan.md` | Design overview and call map |
| `project/test/wps/WP24/test_generate_full_artifact.py` | E2E test: validate full artifact from inputs |

---

## 🧭 User Journey Entry Points for WP24 Toolchain

The `generate_full_artifact_chain` toolchain is triggered in these user flows:

| Scenario | Trigger Source | Description |
|----------|----------------|-------------|
| Full artifact draft | User types \"generate full Risk Plan\" or GPT recommends based on context | Starts planner flow for all required sections |
| Autopilot/quick mode | PM uploads all inputs and wants fast draft | Bypasses manual prompts and runs all sections |
| Multi-section planner | GPT configures flow using template | Uses gate template + section list to auto-run generation |

---

## 🚦 User Journey Exit + Handoff

Upon completion, the toolchain returns:

| Step | Output | Handoff Target |
|------|--------|----------------|
| Final draft per section | Updates `ArtifactSection.text`, `version`, `status` | Used by `assemble_artifact_chain` |
| Reasoning logs | Updates `ReasoningTrace.steps`, `draft_chunks` | Enables trace-based explanations or redos |
| Prompt summaries | New `PromptLog` entries per section | Used for QA and prompt tuning |
| Assembled artifact | Output to `DocumentVersionLog`, Google Drive link | User receives draft link |
| Chain summary | Final JSON response with trace, summary, document info | Passed to GPT for status narration or follow-up questions |

---

## 🗃️ Database Tables: Read/Write Scope for WP24

| Table | Read/Write | Usage |
|-------|------------|-------|
| `ProjectProfile` | Read | Gate type, project context |
| `ArtifactSection` | Write | Create and update section drafts |
| `PromptLog` | Write | Log LLM calls per section |
| `ReasoningTrace` | Write | Summarize logic, sources, and sequence |
| `DocumentVersionLog` | Write | Store Drive/export version of artifact |
| `TaskMetadata` | Write | Log planner chain run, outcomes, failures |

---

## ⚙️ Technical Design Notes

- **Planner Scope**: Reads gate template from `gate_reference.yaml`, selects required sections.
- **Toolchain**: For each section, calls `generate_section_chain`, waits for result, logs.
- **Error Handling**: Catches LLM timeouts or token overflows; logs to `TaskMetadata.errors`.
- **Assembly**: Once sections complete, calls `assemble_artifact_chain` → outputs Drive file.
- **Handoff**: Returns full summary to GPT for narration, validation, or user confirmation.
- **Hooks**: Integrates `createSessionSnapshot` after section 1 for resumability.

### 🧠 Token + Timeout Safeguards

- Use `get_token_usage` pre-check per section input block
- Limit batch inputs using `max_chunk_tokens = 1200`
- Enable retry logic with exponential backoff (3 max attempts)
- Use `draft_chunks` field in `ReasoningTrace` to log partial output
- On failure, record `TaskMetadata.status = failed`, preserve last step in trace
- Recommend `summarize_memory` if project corpus is too large to fit

---

## ✅ Task Breakdown

| Task | Owner | File(s) |
|------|-------|---------|
| Plan YAML + flow map | WP24 | `WP24_toolchain_plan.md` |
| Build orchestration | WP24 | `generate_full_artifact_chain.py` |
| Section iteration | WP24 | Wrapper for `generate_section_chain` |
| Output write hooks | WP24 | Write to `ArtifactSection`, `DocumentVersionLog` |
| Logging | WP24 | Update `ReasoningTrace`, `PromptLog`, `TaskMetadata` |
| Testing | WP24 | `test_generate_full_artifact.py` |

---

## 🔁 Toolchain Integration
- Drives section generation via `generate_section_chain`
- Leverages ReasoningTrace + PromptLog for auditability
- Finalizes with `assemble_artifact_chain`
- Optional: use `createSessionSnapshot` to support resume or rollback

---

## 🧪 Testing
| File Path | Description |
|-----------|-------------|
| `project/test/wps/WP24/test_generate_full_artifact.py` | Runs full test with sample gate + 3+ sections |

---

## 🔮 Future Extensions
- Allow async section generation with queue-based dispatch
- Enable user preview/review per section before commit
- Add artifact-level summary metrics (completeness, confidence)
- Visual display of generation status for UI pods
- Use planner profile (e.g., tone, review role) to guide formatting