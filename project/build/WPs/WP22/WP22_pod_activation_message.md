### 📦 Work Package Activation

**To:** `WP22Pod`

**From:** Lead Pod (via Human Lead)

**Subject:** Activate `WP22 – GoC Alignment Search Tool`

---

### 🔍 Context
We are kicking off `WP22 – GoC Alignment Search Tool`, part of the Phase 2 expansion to strengthen artifact generation through alignment to government priorities. This tool supports section-level evidence development and planning workflows by identifying references in mandate letters, strategies, and government-wide plans.

This toolchain step will allow us to:
- Search both embedded corpora and live GoC web content
- Summarize policy and strategy alignment to current section draft
- Feed structured results to downstream tools like `section_synthesizer`
- Log findings in PromptLog and ReasoningTrace for traceability

---

### 🗿 Instructions
1. Review your WP scope and deliverables (system/fetchFile: `project/build/wps/WP22/WP22_definition.md`)
2. Read the design note for integration strategy: `WP22_design_note.md`
3. Fetch reference files (see below)
4. Draft design plan and task list. Commit to: `project/build/wps/WP22/`
5. Build and test deliverables
6. Request Human Lead review and provide midpoint + final updates to Pod Lead

---

### 📂 Repo + Branch Info
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Project Folder:** `project/build/wps/WP22/`
- **Task ID:** `2.2_build_and_patch`

---

### Key Reference Files
- project/build/wps/WP22/WP22_definition.md
- project/build/wps/WP22/WP22_design_note.md
- app/tools/tool_wrappers/loadCorpus.py
- app/engines/toolchains/generate_section_chain.py
- app/db/models/PromptLog.py
- app/db/models/ReasoningTrace.py
- project/reference/tool_catalog.yaml
- project/reference/gpt_tools_manifest.json
- project/system_design/dense_artifact_generation.md

---

### Key Deliverables
- `goc_alignment_search.py`
- `queryCorpus.py`
- `goc_alignment_prompts.yaml`
- Integration with planner + generate_section_chain

---

### 🚀 Working With the Human Lead
- Coordinate at plan, build, test, and final checkpoints
- Await plan approval before building deliverables
- Commit files and share links for review
- Human Lead will validate DB and planner integration
- Provide final results and handoff summary to Lead Pod

---

Let alignment begin 🎯