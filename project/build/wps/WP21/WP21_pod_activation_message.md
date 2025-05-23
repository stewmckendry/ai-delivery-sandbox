### 📦 Work Package Activation

**To:** `WP21Pod`

**From:** Lead Pod (via Human Lead)

**Subject:** Activate `WP21 – Spillover Tools and Memory Enhancements`

---

### 🔍 Context
You are activated to capture and implement critical tooling and enhancements that were deferred from Phase 1 or introduced in WP12’s design patch. These tools and schema updates bridge input capture with planner orchestration and memory review.

---

### 🗿 Instructions
1. Review your WP scope and deliverables (system/fetchFile: `project/build/wps/WP21/WP21_definition.md`)
2. Fetch reference files listed below.
3. Build plan + tasks. Commit to: `project/build/wps/WP21/`
4. Coordinate with Human Lead to build and test incrementally.

---

### 📂 Repo + Branch Info
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Project Folder:** `project/build/wps/WP21/`
- **Task ID:** `2.2_build_and_patch`

---

### Reference Materials to Fetch
- `project/build/wps/WP21/WP21_definition.md`
- `project/system_design/dense_artifact_generation.md`
- `project/build/design_decisions_log.md`
- `project/reference/tool_catalog.yaml`
- `project/reference/gpt_tools_manifest.json`
- `project/system_design/session_memory_model_v2.md`

---

### 📦 Deliverables (from WP Definition)
- `queryCorpus` tool
- PromptLog schema updates
- LLM-enhanced inputChecker patch
- GPT tool manifest update

---

### 🧠 Lessons Learned (from Phase 1)
- Tool validation hooks are critical — reuse registry patterns
- Manifest should match OpenAPI style to interop with GPT
- Watch for schema drift: coordinate with WP2/WP4/WP9

---

### 🚀 Working With the Human Lead
Follow SOP in: `project/build/build_pods_sop.md`  
Use commit_and_log for all file operations and coordination check-ins.

---

Onward to the spillover frontier 🛠️