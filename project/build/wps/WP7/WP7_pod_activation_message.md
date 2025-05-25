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
1. Review your WP definition (system/fetchFile: `project/build/wps/WP7/WP7_definition.md`)
2. Fetch supporting reference files listed below.
3. Write plan + task list. Commit to: `project/build/wps/WP7/`
4. Coordinate with Human Lead for build/test phases.

---

### 📂 Repo + Branch Info
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Project Folder:** `project/build/wps/WP7/`
- **Task ID:** `2.2_build_and_patch`

---

### Reference Materials to Fetch
- `project/build/wps/WP7/WP7_definition.md`
- `project/reference/project_profile.yaml`
- `project/discovery/policygpt_user_journeys.md`
- `project/discovery/acceptance_criteria.md`
- `project/system_design/session_memory_model_v2.md`
- `project/system_design/system_architecture_v2.md`

---

### 📦 Deliverables (from WP Definition)
- `ProjectProfile` model
- `project_profile_updater.py`
- `show_profile.py` tool
- Profile reference docs and flow map

---

### 🧠 Lessons Learned (from Phase 1)
- Profile should evolve over session, not be static
- Use memory + database for persistence
- Ensure tools can update and read profile mid-session

---

### 🚀 Working With the Human Lead
Follow SOP in: `project/build/build_pods_sop.md`
Commit files using commit_and_log and share Git links. Review with Human Lead at each milestone.

---

Profile power, activate 🧬