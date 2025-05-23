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

What is PolicyGPT?
- PolicyGPT is a custom GPT + toolchain designed to support government teams in drafting, editing, and finalizing gate-based documentation at the quality required for approval of multi-million dollar public programs and infrastructure.
- Discovery and system design and work package planning are complete and fully documented.  Build is in progress and being executed through a series of work packages.


---

### 🗿 Instructions
1. Review your WP scope and deliverables (system/fetchFile: `project/build/wps/WP17b/WP17b_definition.md`)
2. Fetch key reference files (see below)
3. Create design plan and task list. Commit to: `project/build/wps/WP17b/`
4. Execute deliverables as listed.
5. Request Human Lead review and start building after approval.
6. Provide updates to Lead Pod at:
   - Kickoff confirmation
   - Midpoint progress + blockers
   - Completion and output link

---

### 📂 Repo + Branch Info
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Project Folder:** `project/build/wps/WP17b/`
- **Task ID:** `2.2_build_and_patch`

---

### Reference Materials to Fetch (batch API call)
Call /system/fetchFiles in batch mode to retrieve the following files (use the above repo_name and branch):
Break the files into groups to avoid size limits.

#### Your Work Assignment (WP9)
project/build/wps/WP17b/WP17b_definition.md

#### Other Work Packages
project/build/wps/work_package_overview.md

#### System Design + Reference Files
project/system_design/dense_artifact_generation.md
project/system_design/system_architecture_v2.md
project/system_design/tool_catalog_v3.md
project/system_design/db_schema_notes_v3.md
project/system_design/session_memory_model_v2.md
project/system_design/api_contracts_v3.md
project/build/tool_creation_guide.md
project/build/wps/WP3b/tool_registry_system.md
project/build/wps/WP3a/WP3a_toolchain_system.md
project/discovery/policygpt_user_journeys.md
project/discovery/project_goals.md
project/reference/gate_reference_v2.yaml
app/tools/tool_wrappers/uploadTextInput.py
app/tools/tool_registry.py
app/engines/api_router.py
app/engines/memory_sync.py
app/engines/planner_orchestrator.py
app/db/database.py
app/db/models/SessionSnapshot.py
app/db/models/PromptLog.py


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
- Follow SOP in: `project/build/build_pods_sop.md`  
- Coordinate at plan, build, test, and final review checkpoints.
- Read message, WP definition, and reference files to get up to speed. Ask the Human Lead questions if anything is unclear.
- Generate a plan and design for WP deliverables. Include assumptions for validation and list inputs needed from Human Lead.  Create a task list to track progress.  Commit the files to `project/build/wps/<wp_id>/` using the commit_and_log tool.
- Await Human Lead approval to begin building deliverables.
- After approval, generate all deliverables listed in the WP definition (in batches if preferred).  
- Commit files to the folders/paths listed in WP definition using the commit_and_log tool.
- Share GitHub file links in chat: `https://github.com/stewmckendry/ai-delivery-sandbox/blob/sandbox-curious-falcon/<path_from_root>`
- Receive Human Lead feedback or OK to proceed to test.
- If setup steps are needed, generate deploy steps and commit to `project/deploy/wps/<wp_id>/`. Share the link.
- Human Lead runs deploy steps and reports back.
- Generate test package (plan, data, CLI scripts or GPT config). Commit to `project/test/<wp_id>/`.
- Human Lead runs tests and reports back results.
- Generate status update for Lead Pod. Include blockers, change requests, or highlights.

---

Let the drafting begin 💥