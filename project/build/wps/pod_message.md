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
1. Review the WP definition and scope.
2. Execute deliverables as listed.
3. Provide updates to Lead Pod at:
   - Kickoff confirmation
   - Midpoint progress + blockers
   - Completion and output link
4. Follow SOP: [`build_pods_sop.md`](../build_pods_sop.md)

### 🧪 Expectations
- Stay aligned with defined scope.
- Raise blockers early.
- Share reasoning for significant changes.

### 📂 Repo + Branch Info
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Project Folder:** `project/build/wps/{{WP ID}}/`
- **Task ID:** `2.2_build_and_patch`

### 📌 Reference Files
- [`{{WP ID}}_definition.md`](./{{WP ID}}_definition.md)
- [`tool_catalog_v2.md`](../tool_catalog_v2.md)
- [`session_memory_model_v2.md`](../session_memory_model_v2.md)
- [`gate_reference.yaml`](../../../reference/gate_reference.yaml)

### 🧠 Reminder
Escalate design mismatches to `DesignPatchPod` (WP12) using logs and summary.

---

### 🚀 Working With the Human Lead
- Read message, WP definition, and reference files to get up to speed. Ask the Human Lead questions if anything is unclear.
- Generate a plan and design for WP deliverables. Include assumptions for validation and list inputs needed from Human Lead.
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

Let the build begin 💥