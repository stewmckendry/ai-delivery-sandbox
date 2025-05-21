## 📨 Pod Activation Message Template

This message format should be used to activate a Work Package (WP) Pod. Customize placeholders with specific values before sending.

---

### 📦 Work Package Activation

**To:** `{{PodName}}`

**From:** Lead Pod (via Human Lead)

**Subject:** Activate `{{WP ID}} – {{WP Name}}`

### 🔍 Context
We are kicking off `{{WP ID}} – {{WP Name}}` as defined in the system architecture. The purpose of this WP is to:
- `{{Summary from WP Outcome}}`

### 📟 Instructions 
1. Review the WP definition and scope. (call system/fetchFile with below repo and branch and file_path: project/build/wps/WP1a/<wp_id>_definition.md)
2. Execute deliverables as listed.
3. Provide updates to Lead Pod at:
   - Kickoff confirmation
   - Midpoint progress + blockers
   - Completion and output link
4. Follow SOP: (call system/fetchFile: project/build/build_pods_sop.md)
(read ### 🚀 Working With the Human Lead for how we work together)

### 🧪 Expectations
- Stay aligned with defined scope.
- Raise blockers early.
- Share reasoning for significant changes.

### 📂 Repo + Branch Info
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Project Folder:** `project/build/wps/{{WP ID}}/`
- **Task ID:** `2.2_build_and_patch`

### Reference Materials
Call /system/fetchFiles in batch mode to retrieve the following files (use the above repo_name and branch):
Break the files into groups to avoid size limits.

#### Your Work Assignment (WP1a)
project/build/wps/WP1a/WP1a_definition.md  

#### Other Work Packages
project/build/wps/work_package_overview.md

#### Pod SOPs + Message Templates
project/build/build_pods_sop.md

#### System Design + Reference Files
project/discovery/project_goals.md
project/discovery/policygpt_user_journeys.md
project/build/acceptance_criteria v2.md
project/build/PolicyGPT_Features v2.md
project/reference/gate_reference_v2.yaml
project/system_design/reference_model_v2.md
project/system_design/tool_catalog_v2.md
project/system_design/session_memory_model_v2.md
project/system_design/data_flow_master_v2.md
project/system_design/api_contracts_v2.md
project/system_design/error_handling_matrix_v2.md
project/system_design/system_architecture_v2.md
project/system_design/gating_doc_quality_v2.md
project/system_design/integration_points_v2.md
project/system_design/db_schema_notes_v2.md


### 🧠 Reminder
Escalate design mismatches to `DesignPatchPod` (WP12) using logs and summary.

---

### 🚀 Working With the Human Lead
- Read message, WP definition, and reference files to get up to speed. Ask the Human Lead questions if anything is unclear.
- Generate a plan and design for WP deliverables. Include assumptions for validation and list inputs needed from Human Lead.  Create a task list to track progress.  Commit to `project/build/wps/<wp_id>/` using the commit_and_log tool.
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

### Rehydration Protocol
If session slows:
- Acknowledge and request a rehydration
- Launch a new instance
- Resume from last committed state
- Notify Lead Pod

---

Let the build begin 💥