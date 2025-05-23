### 📦 Work Package Activation

**To:** `WP17bPod`

**From:** Lead Pod (via Human Lead)

**Subject:** Activate `WP17b – Section Draft Generation from Inputs`

---

### 🔍 Context
We are kicking off `WP17b – Section Draft Generation from Inputs`, part of the Phase 2 pipeline to transform captured user inputs into structured section drafts. This work supports modular drafting of gate documents, aligned with the `dense_artifact_generation.md` design.

You are responsible for building tools and planner logic that:
- Use `PromptLog` entries and memory embeddings
- Trigger the `compose_and_cite` toolchain
- Store results in `ArtifactSection`
- Log steps in `ReasoningTrace`

---

### 🗿 Instructions
1. Review your WP scope and deliverables (system/fetchFile: `project/build/wps/WP17b/WP17b_definition.md`)
2. Fetch key reference files (see below)
3. Create design plan and task list. Commit to: `project/build/wps/WP17b/`
4. Request Human Lead review and start building after approval.

---

### 📂 Repo + Branch Info
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Project Folder:** `project/build/wps/WP17b/`
- **Task ID:** `2.2_build_and_patch`

---

### Reference Materials to Fetch (batch API call)
- `project/build/wps/WP17b/WP17b_definition.md`
- `project/system_design/dense_artifact_generation.md`
- `project/reference/tool_catalog.yaml`
- `project/system_design/session_memory_model_v2.md`
- `project/discovery/acceptance_criteria.md`
- `project/discovery/policygpt_user_journeys.md`
- `project/system_design/system_architecture_v2.md`

---

### 📦 Deliverables (from WP Definition)
- `app/tools/tool_wrappers/compose_and_cite.py`
- `project/prompts/section_drafting_prompt.md`

---

### 🧠 Lessons Learned (from Phase 1)
- Start with a CLI-first working pipeline
- Ensure schema field alignment early
- Use Git-hosted reference data
- Keep modular tools and reusable prompts

---

### 🚀 Working With the Human Lead
Follow SOP in: `project/build/build_pods_sop.md`  
Use commit_and_log tool to save files and share GitHub links.  
Coordinate at plan, build, test, and final review checkpoints.

---

Let the drafting begin 💥