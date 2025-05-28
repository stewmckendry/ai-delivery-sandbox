## 🧭 WP27 Iteration 2 Plan

**Branch:** `sandbox-curious-falcon`  
**Path:** `project/build/wps/WP27/plan_iteration_2.md`  
**Goal:** Improve section quality, guidance, and grounding for more relevant and context-aware output.

### 🎯 Objectives
- Improve **relevance** and **grounding** of generated sections.
- Enhance **logging clarity** and **observability** across the toolchain.
- Replace rigid **intent-checking** with LLM-backed guidance.
- Confirm **project profile** is correctly captured in upload tools or flow.

### 🔁 Flow Enhancements

| Step | Enhancement |
|------|-------------|
| Ingestion | Ensure project profile is saved during upload phase or updated to use toolchain explicitly. |
| Input Checker | Replace strict keyword intent check with LLM-based feedback on missing inputs. |
| Section Generator | Improve grounding by using project profile more explicitly in prompt construction. |
| Observability | Simplify logging; emit clear, prefixed steps + outputs for user inspection. |

### 🧪 Evaluation Plan
Same structure as Iteration 1, plus:
- Validate improved alignment between test input and generated section.
- Capture logs/output for each step for side-by-side comparison.

### 🧰 Tools & Chains
- `uploadTextInput`
- `inputChecker` (patched to LLM-based)
- `generate_section_chain` (updated for grounding/logging)

### ✅ Success Criteria
- Output directly addresses uploaded input.
- Missing info guidance is helpful.
- Logs clearly show progress + results of each step.