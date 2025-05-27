### 📦 Work Package Activation

**To:** `WP24Pod`

**From:** Lead Pod (via Human Lead)

**Subject:** Activate `WP24 – Autopilot: Full Artifact Generator`

---

### 🔍 Context
We are kicking off `WP24 – Autopilot: Full Artifact Generator`, part of Phase 2. This WP will enable a one-shot document generation toolchain for PMs who have uploaded all inputs and want to generate gate artifacts in a single flow.

This supports Journey C (Autopilot Mode) from the UX design.

---

### 🧠 Objective
Implement the `generate_full_artifact_chain` toolchain that:
- Plans all sections
- Iterates `generate_section_chain`
- Assembles using `assemble_artifact_chain`
- Commits to Drive + DB with trace logs

---

### 🗿 Instructions
1. Review `WP24_definition.md`
2. Draft plan in: `project/build/wps/WP24/WP24_toolchain_plan.md`
3. Build orchestration toolchain + tests
4. Validate end-to-end outputs, including DB and Drive

---

### 📂 Repo + Branch Info
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Project Folder:** `project/build/wps/WP24/`
- **Task ID:** `2.2_build_and_patch`

---

### Key Files to Reference
- `project/system_design/dense_artifact_generation.md`
- `project/build/wps/WP12/WP12_ux_design_review.md`
- `app/engines/toolchains/generate_section_chain.py`
- `app/engines/toolchains/assemble_artifact_chain.py`
- `project/reference/gate_reference.yaml`

---

### 🚀 Guidance
- Start with hardcoded gate (e.g., Risk Plan)
- Enable logging of each section’s outcome
- Build in retry + error capture hooks

Get ready for liftoff 🚀