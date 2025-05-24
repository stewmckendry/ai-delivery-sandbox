### 📦 Work Package Activation

**To:** `WP18Pod`

**From:** Lead Pod (via Human Lead)

**Subject:** Activate `WP18 – Artifact Assembly and Routing`

---

### 🔍 Context
We are activating `WP18 – Artifact Assembly and Routing`, part of the document generation pipeline. You will build the toolchain to combine drafted sections into complete gate artifacts, validate their completeness, and prepare them for routing to Drive and other destinations.

You own the tools that assemble and commit the final artifact, aligned to `gate_reference_v2.yaml` and `dense_artifact_generation.md`.

What is PolicyGPT?
- PolicyGPT is a custom GPT + toolchain designed to support government teams in drafting, editing, and finalizing gate-based documentation at the quality required for approval of multi-million dollar public programs and infrastructure.

Other Background:
- Discovery and system design and work package planning are complete and fully documented.  Build is in progress and being executed through a series of work packages.
- This work builds on `WP17b`, which introduced structured `ArtifactSection` entries, each containing a drafted section with paragraph-level chunking and versioned ReasoningTrace metadata.
- The goal of this WP is to enable the system to assemble drafted sections into complete artifacts and route them to the correct destinations (e.g., for review, approval, storage). This includes validation, sequencing, and formatting.  It will use the same toolchain system as `WP17b`, but with a focus on the final assembly and routing of artifacts.
- Sections can be queried by `artifact_id`, `gate_id`, and `section_id` and sorted for assembly using `gate_reference_v2.yaml`.


---

### 🗿 Instructions
1. Review your WP scope and deliverables (system/fetchFile: `project/build/wps/WP8/WP18_definition.md`)
2. Fetch key reference files (see below)
3. Create design plan and task list. Commit to: `project/build/wps/WP18/`
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
- **Project Folder:** `project/build/wps/WP18/`
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

## 🧠 Expanded Lessons Learned

- Keep input/output traceable to gates and sections
- Use DB schemas as source of truth
- Validate artifact completeness against schema early
- Use `ReasoningTrace` to store toolchain step-by-step logs
- Chunk long outputs for traceability and UI interaction
- Validate tool outputs with Pydantic schemas
- Register toolchains + tools cleanly to support planner invocation
- Use `gate_reference.yaml` to drive logic across sections
- Think through output versions: what, why, and how to store

---

### 🚀 Working With the Human Lead
Follow SOP in: `project/build/build_pods_sop.md`
Use commit_and_log tool and GitHub links.
Coordinate for reviews and testing.

---

Let’s get assembling 🔧