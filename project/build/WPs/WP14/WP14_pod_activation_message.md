### 📦 Work Package Activation

**To:** `WP14Pod`

**From:** Lead Pod (via Human Lead)

**Subject:** Activate `WP14 – External Search Tool for Artifact Drafting`

---

### 🔍 Context
We are kicking off `WP14 – External Search Tool for Artifact Drafting`, part of the Phase 2 pipeline to integrate external research inputs into section and artifact generation as part of PolicyGPT. This work supports enhanced evidence-gathering for gate documents, aligned with the `generate_section` toolchain and `dense_artifact_generation.md` architecture.

You are responsible for building a modular search tool and integrating it into planner logic that:
- Performs targeted web or academic search
- Supports multiple search types (e.g. general web, jurisdiction scan, market scan)
- Normalizes and summarizes the results
- Returns them in a format usable by downstream tools (e.g., `section_synthesizer`)
- Logs all search operations

What is PolicyGPT?
- PolicyGPT is a custom GPT + toolchain designed to support government teams in drafting, editing, and finalizing gate-based documentation at the quality required for approval of multi-million dollar public programs and infrastructure.
- Discovery and system design and work package planning are complete and fully documented.  Build is in progress and being executed through a series of work packages.


---

### 🗿 Instructions
1. Review your WP scope and deliverables (system/fetchFile: `project/build/wps/WP14/WP14_definition.md`)
2. Fetch key reference files (see below)
3. Create design plan and task list. Commit to: `project/build/wps/WP14/`
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
- **Project Folder:** `project/build/wps/WP14/`
- **Task ID:** `2.2_build_and_patch`

---

### Reference Materials to Fetch
Call /system/fetchFiles in batch mode to retrieve:
- project/build/wps/WP14/WP14_definition.md
- project/build/wps/WP14/WP14_definition_searchTypes.md
- project/build/wps/work_package_overview.md
- project/system_design/dense_artifact_generation.md
- project/system_design/tool_catalog_v3.md
- project/system_design/system_architecture_v2.md
- app/tools/tool_wrappers/section_synthesizer.py
- app/engines/toolchains/generate_section_chain.py
- app/engines/planner_orchestrator.py
- app/db/models/PromptLog.py
- app/db/models/ReasoningTrace.py
- app/db/models/ArtifactSection.py
- project/reference/gpt_tools_manifest.json
- project/reference/tool_catalog.yaml
- project/reference/gate_reference_v2.yaml

---

### 📦 Deliverables (from WP Definition)
- `app/tools/tool_wrappers/web_search.py`
- `search_handlers/<type>.py`
- `project/prompts/search_prompts.yaml`
- `project/build/wps/WP14/WP14_toolchain_integration_note.md`

---

### 🧠 Lessons Learned (from Phase 1 + WP17b)
- Tool output must align with toolchain input schemas
- Planner routing should use intent and inject structured metadata
- Log tool usage in PromptLog for traceability
- Build for extensibility (e.g., new search types or prompt formats)

---

### 🚀 Working With the Human Lead
- Follow SOP in: `project/build/build_pods_sop.md`
- Coordinate at plan, build, test, and final review checkpoints.
- Generate a plan and design for WP deliverables. Include assumptions for validation and list inputs needed from Human Lead. Commit files to `project/build/wps/WP14/`
- Await approval to begin building deliverables
- Commit deliverables to listed paths
- Share GitHub file links in chat
- Human Lead will run deploy and test scripts
- Report back test results, blockers, or learnings to Lead Pod

---

Let the searching begin 🔍