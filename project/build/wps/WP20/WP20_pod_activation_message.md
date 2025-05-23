### 📦 Work Package Activation

**To:** `WP20Pod`

**From:** Lead Pod (via Human Lead)

**Subject:** Activate `WP20 – Google Drive Storage Integration`

---

### 🔍 Context
This work package connects PolicyGPT's document pipeline to Google Drive. You'll build tools that allow the system to export and retrieve documents from structured Drive folders.

This enables cross-org collaboration and long-term storage, supporting both markdown and PDF formats.

---

### 🗿 Instructions
1. Review your WP scope and deliverables (system/fetchFile: `project/build/wps/WP20/WP20_definition.md`)
2. Fetch key reference files (see below)
3. Draft a plan and implementation steps. Commit to: `project/build/wps/WP20/`
4. Begin deliverables after Human Lead approval.

---

### 📂 Repo + Branch Info
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Project Folder:** `project/build/wps/WP20/`
- **Task ID:** `2.2_build_and_patch`

---

### Reference Materials to Fetch
- `project/build/wps/WP20/WP20_definition.md`
- `project/system_design/dense_artifact_generation.md`
- `project/reference/tool_catalog.yaml`
- `project/system_design/integration_points_v2.md`
- `project/system_design/db_schema_notes_v3.md`

---

### 📦 Deliverables (from WP Definition)
- `app/tools/tool_wrappers/storeToDrive.py`
- `app/tools/tool_wrappers/fetchFromDrive.py`
- `project/config/drive_structure.yaml`

---

### 🧠 Lessons Learned (from Phase 1)
- Use service account auth securely
- Add file overwrite detection to avoid version confusion
- Store Drive URLs in DB for downstream tools

---

### 🚀 Working With the Human Lead
Follow SOP in: `project/build/build_pods_sop.md`
Commit all updates and share GitHub links. Coordinate for deploy and test steps.

---

Ready to launch to Drive ☁️