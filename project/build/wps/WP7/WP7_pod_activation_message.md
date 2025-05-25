### 📦 Work Package Activation

**To:** `WP7Pod`

**From:** Lead Pod (via Human Lead)

**Subject:** Activate `WP7 – Project Profile Engine`

---

### 🔍 Context
PolicyGPT now supports dynamic project profiles that adjust drafting and validation logic based on the context of a public infrastructure initiative. WP7 implements the engine that stores, updates, and exposes this live configuration state.

What is PolicyGPT?
- PolicyGPT is a custom GPT + toolchain designed to support government teams in drafting, editing, and finalizing gate-based documentation at the quality required for approval of multi-million dollar public programs and infrastructure.
- Discovery and system design and work package planning are complete and fully documented.  Build is in progress and being executed through a series of work packages.

---

### 🗿 Instructions
1. Review your WP scope and deliverables (system/fetchFile: `project/build/wps/WP7/WP7_definition.md`)
2. Fetch key reference files (see below)
3. Create design plan and task list. Commit to: `project/build/wps/WP7/`
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
- **Project Folder:** `project/build/wps/WP7/`
- **Task ID:** `2.2_build_and_patch`

---

### Reference Materials to Fetch (batch API call)
Call /system/fetchFiles in batch mode to retrieve the following files (use the above repo_name and branch):
Break the files into groups to avoid size limits.

#### Your Work Assignment (WP18)
project/build/wps/WP18/WP18_definition.md

#### Other Work Packages & Tools
project/build/work_package_tracker.md
project/build/tool_implementation_tracker.md

#### System Design + Reference Files
project/system_design/dense_artifact_generation.md
project/build/wps/WP17b/toolchain_registration_guide.md
project/build/wps/WP17b/WP17b_exit_report.md
project/build/wps/WP17b/WP17b_exit_report_part2.md
project/build/wps/WP17b/WP17b_chunking_and_schema_notes.md
project/system_design/db_schema_notes_v3.md
project/system_design/system_architecture_v2.md
project/system_design/tool_catalog_v3.md
project/system_design/session_memory_model_v2.md
project/system_design/api_contracts_v3.md
project/build/tool_creation_guide.md
project/build/wps/WP3b/tool_registry_system.md
project/discovery/policygpt_user_journeys.md
project/discovery/project_goals.md
project/reference/gate_reference_v2.yaml
app/engines/toolchains/generate_section_chain.py
app/tools/tool_wrappers/memory_retrieve.py
app/tools/tool_wrappers/section_synthesizer.py
app/tools/tool_wrappers/section_refiner.py
app/tools/tool_wrappers/uploadTextInput.py
app/tools/tool_registry.py
app/engines/api_router.py
app/engines/memory_sync.py
app/engines/planner_orchestrator.py
app/db/database.py
app/db/models/ArtifactSection.py
app/db/models/ReasoningTrace.py
app/db/models/PromptLog.py


---

### 🧠 Lessons Learned (from Phase 1)
- Profile should evolve over session, not be static
- Use memory + database for persistence
- Ensure tools can update and read profile mid-session

---

### 🚀 Working With the Human Lead
- Follow SOP in: `project/build/build_pods_sop.md`  
- Coordinate at plan, build, test, and final review checkpoints.
- Read message, WP definition, and reference files to get up to speed. Ask the Human Lead questions if anything is unclear.
- Generate a plan and design for WP deliverables. Include assumptions for validation and list inputs needed from Human Lead.  Create a task list to track progress.  Commit the files to `project/build/wps/WP7/` using the commit_and_log tool.
- Await Human Lead approval to begin building deliverables.
- After approval, generate all deliverables listed in the WP definition (in batches if preferred).  
- Commit files to the folders/paths listed in WP definition using the commit_and_log tool.
- Share GitHub file links in chat: `https://github.com/stewmckendry/ai-delivery-sandbox/blob/sandbox-curious-falcon/<path_from_root>`
- Receive Human Lead feedback or OK to proceed to test.
- If setup steps are needed, generate deploy steps and commit to `project/deploy/wps/WP7/`. Share the link.
- Human Lead runs deploy steps and reports back.
- Generate test package (plan, data, CLI scripts or GPT config). Commit to `project/test/WP7/`.
- Human Lead runs tests and reports back results.
- Generate status update for Lead Pod. Include blockers, change requests, or highlights.

---

Profile power, activate 🧬