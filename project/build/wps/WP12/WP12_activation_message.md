## Activation Message: WP12 – System Design Patch Pod

**Pod:** WP12Pod
**Task ID:** 2.2_build_and_patch
**Repo:** ai-delivery-sandbox  
**Branch:** sandbox-curious-falcon  
**Project Folder:** `project/build/wps/WP12/`

---

### Objective
Investigate and resolve an open design issue: **Where and how is the artifact draft generated in PolicyGPT?**

### Background
Several Pods have delivered related components:
- **WP16**: Input UI layer and session scaffolding
- **WP9**: Upload tools, ingestion logs, PromptLog + SessionSnapshot
- **WP3b**: Toolchain registry and tool manifest
- **WP1a**: Document scaffolding and assembly
- **WP3a**: Planner + memory orchestration

But it is unclear where the drafting actually happens:
- In the **ChatGPT UI** with LLM assistance?
- In the **backend** using tools like `compose_and_cite`?
- Or both, in a coordinated hybrid?

### Key Questions to Answer
1. What component is responsible for draft synthesis of gate artifacts?
2. How does session memory contribute to drafting?
3. How should this be coordinated between toolchain, session memory, and UI?
4. Does this support user needs for rich, high-quality documentation under gating standards?

### Files to Review
- `project/system_design/system_architecture_v2.md`
- `project/system_design/session_memory_model_v2.md`
- `project/system_design/data_flow_master_v2.md`
- `project/build/PolicyGPT_Features v2.md`
- `project/system_design/gating_doc_quality_v2.md`
- `project/system_design/db_schema_notes_v2.md`
- `project/build/system_risks_and_questions.md`

### Constraints & Considerations
- Deep research quality and structured gating outputs
- Token limits and session memory compression
- Real-time vs. staged generation experience
- Integration with GPT-based UX in WP16

### Next Step
Please review the above, propose a system design solution, and respond in a design patch format.
We recommend updating the data flow diagram and writing a markdown summary.

Thank you!