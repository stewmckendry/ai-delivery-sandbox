### 📦 Work Package Activation

**To:** `WP26Pod`

**From:** Lead Pod (via Human Lead)

**Subject:** Activate `WP26 – Composable Planner: User-Configurable Chain Builder`

---

### 🔍 Context
We are kicking off `WP26 – Composable Planner`, part of Phase 4 to empower users and GPT to configure the steps used in generating gate artifacts. This work introduces a flexible, template-based planner to replace hardcoded toolchains.

This supports the final UX journey outlined in `WP12_ux_design_review.md`.

---

### 🧠 Objective
Build a YAML-based planner and execution engine that:
- Accepts user/GPT plan configuration
- Loads toolchain templates
- Executes configured steps
- Logs trace for every operation

---

### 🗿 Instructions
1. Review `WP26_definition.md`
2. Draft plan in `WP26_planner_architecture.md`
3. Implement `composable_planner.py` + test harness
4. Create example templates for Risk Plan, Funding Memo
5. Validate outputs across several plan variations

---

### 📂 Repo + Branch Info
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Project Folder:** `project/build/wps/WP26/`
- **Task ID:** `2.2_build_and_patch`

---

### Key Files to Reference
- `project/system_design/dense_artifact_generation.md`
- `project/build/wps/WP12/WP12_ux_design_review.md`
- `project/reference/tool_catalog.yaml`
- `project/reference/gpt_tools_manifest.json`

---

### 🚀 Guidance
- Use system prompts to cue planner config dialogue
- Design templates to be easy-to-extend
- Ensure clear failure messages and step visibility

Compose and conquer 🧩