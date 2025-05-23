### 📦 Work Package Activation

**To:** `WP18Pod`

**From:** Lead Pod (via Human Lead)

**Subject:** Activate `WP18 – Artifact Assembly and Routing`

---

### 🔍 Context
We are activating `WP18 – Artifact Assembly and Routing`, part of the document generation pipeline. You will build the toolchain to combine drafted sections into complete gate artifacts, validate their completeness, and prepare them for routing to Drive and other destinations.

You own the tools that assemble and commit the final artifact, aligned to `gate_reference.yaml` and `dense_artifact_generation.md`.

---

### 🗿 Instructions
1. Review your WP scope and deliverables (system/fetchFile: `project/build/wps/WP18/WP18_definition.md`)
2. Fetch key reference files (see below)
3. Draft plan and task list. Commit to: `project/build/wps/WP18/`
4. Begin deliverables upon Human Lead review.

---

### 📂 Repo + Branch Info
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Project Folder:** `project/build/wps/WP18/`
- **Task ID:** `2.2_build_and_patch`

---

### Reference Materials to Fetch
- `project/build/wps/WP18/WP18_definition.md`
- `project/system_design/dense_artifact_generation.md`
- `project/reference/tool_catalog.yaml`
- `project/reference/gate_reference_v2.yaml`
- `project/discovery/acceptance_criteria.md`

---

### 📦 Deliverables (from WP Definition)
- `app/tools/tool_wrappers/assembleDraft.py`
- `app/tools/tool_wrappers/commitArtifact.py`
- `project/reference/artifact_templates/`

---

### 🧠 Lessons Learned (from Phase 1)
- Keep input/output traceable to gates and sections
- Use DB schemas as source of truth
- Validate artifact completeness against schema early

---

### 🚀 Working With the Human Lead
Follow SOP in: `project/build/build_pods_sop.md`
Use commit_and_log tool and GitHub links.
Coordinate for reviews and testing.

---

Let’s get assembling 🔧