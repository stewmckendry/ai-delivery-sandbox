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