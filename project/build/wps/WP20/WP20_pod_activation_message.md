### 📦 Work Package Activation

**To:** `WP20Pod`

**From:** Lead Pod (via Human Lead)

**Subject:** Activate `WP20 – Google Drive Storage Integration`

---

### 🔍 Context
This work package connects PolicyGPT's document pipeline to Google Drive. You'll build tools that allow the system to export and retrieve documents from structured Drive folders.

This enables cross-org collaboration and long-term storage, supporting both markdown and PDF formats.

What is PolicyGPT?
- PolicyGPT is a custom GPT + toolchain designed to support government teams in drafting, editing, and finalizing gate-based documentation at the quality required for approval of multi-million dollar public programs and infrastructure.
- Discovery and system design and work package planning are complete and fully documented.  Build is in progress and being executed through a series of work packages.


---

### 🗿 Instructions
1. Review your WP scope and deliverables (system/fetchFile: `project/build/wps/WP20/WP20_definition_v2.md`)
2. Fetch key reference files (see below)
3. Create design plan and task list. Commit to: `project/build/wps/WP20/`
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
- **Project Folder:** `project/build/wps/WP20/`
- **Task ID:** `2.2_build_and_patch`

---

### Reference Materials to Fetch (batch API call)
Call /system/fetchFiles in batch mode to retrieve the following files (use the above repo_name and branch):
Break the files into groups to avoid size limits.

#### Your Work Assignment (WP20)
project/build/wps/WP20/WP20_definition_v2.md

#### Other Work Packages & Tools
project/build/work_package_tracker.md
project/build/tool_implementation_tracker.md

#### System Design + Reference Files
app/tools/tool_wrappers/commitArtifact.py – the placeholder to replace
app/engines/toolchains/assemble_artifact_chain.py - the toolchain commitArtifact is part of
app/db/models/DocumentVersionLog.py – Drive URL lives here
project/build/wps/WP18/WP18_exit_report.md – summary of WP18 context
project/system_design/dense_artifact_generation.md – E2E doc pipeline
project/test/WP18/test_runner_assemble_artifact.py – shows call pattern
project/build/wps/WP17b/toolchain_registration_guide.md - toolchain framework 
app/engines/planner_orchestrator.py – planner orchestrator
project/system_design/db_schema_notes_v3.md - DB schema
project/system_design/system_architecture_v2.md
project/system_design/tool_catalog_v3.md
project/build/wps/WP3b/tool_registry_system.md
project/discovery/policygpt_user_journeys.md
project/discovery/project_goals.md
project/reference/gate_reference_v2.yaml
app/tools/tool_registry.py
app/engines/api_router.py
app/engines/memory_sync.py
app/engines/planner_orchestrator.py
app/db/database.py
app/db/models/ArtifactSection.py
app/db/models/ReasoningTrace.py
app/db/models/PromptLog.py

Web: Google Drive API Python SDK docs – for auth + upload
https://developers.google.com/drive/api/guides

---

## 📚 Lessons Learned for WP20 (from WP18)

### 🔄 System Design Alignment
- Build directly on the `assemble_artifact` pipeline using consistent toolchain and validation patterns.
- Ensure tools are modular and use schemas for input/output validation (via Pydantic).

### 🔑 Authentication & Access
- Managing OAuth credentials securely is critical; use environment configs and limit permissions.
- Test token refresh and error handling early to avoid blocking runtime failures.

### 📁 File Management
- Structure folder paths clearly by project, gate, and artifact to ensure traceability.
- Handle overwrite scenarios carefully — include timestamped versions if needed.

### 🧠 Toolchain Logging
- Use `log_tool_usage()` and `save_document_and_trace()` for every tool step to maintain traceability.
- Capture Drive upload outcomes and errors in structured logs.

### 📄 Document Usability
- Users expect clean document formats — maintain markdown/PDF clarity during upload.
- Support section-level fetch to avoid token/API limits in GPT integration.

### 🚧 Testing & Fail-Safes
- Validate integration with Drive sandbox before production scope.
- Build CLI scripts for test uploads, fetches, and error simulations.

### 🧩 Future-Proofing
- Maintain backward compatibility with WP18’s `commitArtifact` for local runs.
- Design folder schema and metadata mapping with scaling in mind (multi-project, multi-org).

---

### 🚀 Working With the Human Lead
- Follow SOP in: `project/build/build_pods_sop.md`  
- Coordinate at plan, build, test, and final review checkpoints.
- Read message, WP definition, and reference files to get up to speed. Ask the Human Lead questions if anything is unclear.
- Generate a plan and design for WP deliverables. Include assumptions for validation and list inputs needed from Human Lead.  Create a task list to track progress.  Commit the files to `project/build/wps/WP20/` using the commit_and_log tool.
- Await Human Lead approval to begin building deliverables.
- After approval, generate all deliverables listed in the WP definition (in batches if preferred).  
- Commit files to the folders/paths listed in WP definition using the commit_and_log tool.
- Share GitHub file links in chat: `https://github.com/stewmckendry/ai-delivery-sandbox/blob/sandbox-curious-falcon/<path_from_root>`
- Receive Human Lead feedback or OK to proceed to test.
- If setup steps are needed, generate deploy steps and commit to `project/deploy/wps/WP20/`. Share the link.
- Human Lead runs deploy steps and reports back.
- Generate test package (plan, data, CLI scripts or GPT config). Commit to `project/test/WP20/`.
- Human Lead runs tests and reports back results.
- Generate status update for Lead Pod. Include blockers, change requests, or highlights.

---

Ready to launch to Drive ☁️