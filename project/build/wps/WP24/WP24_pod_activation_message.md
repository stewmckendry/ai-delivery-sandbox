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
1. Review your WP scope and deliverables (system/fetchFile: `project/build/wps/WP24/WP24_definition.md`)
2. Fetch reference files (see below)
3. Draft design plan and task list. Commit to: `project/build/wps/WP24/`
4. Build and test deliverables
5. Request Human Lead review and provide midpoint + final updates to Pod Lead

---

### 📂 Repo + Branch Info
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Project Folder:** `project/build/wps/WP24/`
- **Task ID:** `2.2_build_and_patch`

---

### Key Files to Reference
- `project/build/wps/WP24/WP24_definition.md`
- `project/system_design/dense_artifact_generation.md`
- `project/build/wps/WP12/WP12_ux_design_review.md`
- `app/engines/planner_orchestrator.py`
- `app/engines/toolchains/assemble_artifact_chain.py`
- `app/engines/toolchains/generate_section_chain.py`
- `app/engines/toolchains/IngestInputChain.py`
- `app/tools/tool_wrappers/memory_retrieve.py`
- `app/tools/tool_wrappers/section_synthesizer.py`
- `app/tools/tool_wrappers/section_refiner.py`
- `app/tools/tool_wrappers/uploadTextInput.py`
- `app/tools/tool_wrappers/loadSectionMetadata.py`
- `app/tools/tool_wrappers/formatSection.py`
- `app/tools/tool_wrappers/mergeSections.py`
- `app/tools/tool_wrappers/finalizeDocument.py`
- `app/tools/tool_wrappers/storeToDrive.py`
- `app/engines/memory_sync.py`
- `app/db/models/ReasoningTrace.py`
- `app/db/models/DocumentVersionLog.py`
- `app/db/models/ArtifactSection.py`
- `app/db/models/WebSearchLog.py`
- `app/db/models/ProjectProfile.py`
- `app/db/models/PromptLog.py`
- `project/reference/tool_catalog.yaml`

---

### 🚀 Guidance
- Start with hardcoded gate (e.g., Risk Plan)
- Enable logging of each section’s outcome
- Build in retry + error capture hooks

Get ready for liftoff 🚀