# WP24 Definition – Autopilot: Full Artifact Generator

## 🧠 Summary
Design and implement a planner-driven toolchain that automates the full generation of a gate artifact from project inputs.

## 🎯 Objective
Build a `generate_full_artifact_chain` toolchain that:
- Enumerates sections from gate template
- Iterates calls to `generate_section_chain`
- Stores ReasoningTrace and validates each section
- Assembles and commits full document

---

## 🧱 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/engines/toolchains/generate_full_artifact_chain.py` | Main orchestration toolchain |
| `project/prompts/full_artifact_generation.yaml` | Planner prompt logic |
| `project/build/wps/WP24/WP24_toolchain_plan.md` | Design overview and call map |

---

## 🔁 Toolchain Integration
- Triggers `generate_section_chain` per artifact section
- Stores all outputs in ArtifactSection + trace
- Assembles with `assemble_artifact_chain`

---

## 🧪 Testing
| File Path | Description |
|-----------|-------------|
| `test_generate_full_artifact.py` | Runs full end-to-end test with 3+ sections |

---

## 🔮 Future Extensions
- Allow section parallelization (queue-based)
- Visual display of section status
- Support abort + resume generation