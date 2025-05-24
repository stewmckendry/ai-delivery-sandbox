# WP18 – Artifact Assembly and Routing

## 🎯 Objective
Enable the system to assemble drafted sections into complete artifacts and route them to the correct destinations (e.g., for review, approval, storage). This includes validation, sequencing, and formatting.
- This work builds on `WP17b`, which introduced structured `ArtifactSection` entries, each containing a drafted section with paragraph-level chunking and versioned ReasoningTrace metadata.
- Sections can be queried by `artifact_id`, `gate_id`, and `section_id` and sorted for assembly using `gate_reference_v2.yaml`.

## 📦 Scope of Work
**In Scope:**
- Stitch individual `ArtifactSection` entries into full artifacts.
- Log to `DocumentVersionLog`.
- Validate artifact completeness against gate_reference_v2.yaml
- Format output as structured markdown or PDF
- Route outputs to next tools or stages (e.g., feedback, Google Drive storage)
- Build `commitArtifact` and `assembleDraft` tools
- Support optional inclusion of `draft_chunks` in output formatting (e.g., for preview tools).
- Parse and format `ReasoningTrace` logs for inclusion in versioning metadata (via `DocumentVersionLog`).
- Support tagging assembled artifacts with latest toolchain and schema versions (from ReasoningTrace).


**Out of Scope:**
- UI for editing the final draft (handled by future front-end WPs)
- Storage mechanics (WP20)

## 🚀 Core Deliverables (Updated)
| File Path | Description |
|-----------|-------------|
| `app/tools/tool_wrappers/assembleDraft.py` | Merges ordered ArtifactSections into a full draft (uses gate_reference + templates) |
| `app/tools/tool_wrappers/commitArtifact.py` | Saves final draft, triggers storage (Google Drive, S3), logs DocumentVersionLog |
| `project/reference/artifact_templates/` | Markdown or Jinja templates per artifact/section type |
| `app/engines/toolchains/assemble_artifact_chain.py` | Defines the ordered toolchain steps for full assembly |
| `app/db/models/DocumentVersionLog.py` | Logs version, timestamp, reason, ReasoningTrace.id per document |
| `app/tools/tool_wrappers/formatSection.py` | Renders a section block using optional template |
| `app/tools/tool_wrappers/mergeSections.py` | Combines formatted blocks into single markdown document |

---

## 📘 Supporting Docs & Assets

### 🛠 Design
| File Path | Description |
|-----------|-------------|
| `project/build/WPs/WP18/WP18_design_plan.md` | High-level architecture, toolchain logic, I/O schema |
| `project/build/WPs/WP18/WP18_template_reference.md` | Sample artifact templates and usage rules |
| `project/build/WPs/WP18/WP18_gate_rendering_map.md` | Map of gate → required sections and order |

### 🧪 Test
| File Path | Description |
|-----------|-------------|
| `project/test/WP18/test_assemble_artifact_plan.md` | Test plan for CLI-based toolchain validation |
| `project/test/WP18/test_assemble_artifact_results.md` | Results file with screenshots, logs, output samples |

### 🚀 Deploy
| File Path | Description |
|-----------|-------------|
| `project/deploy/WP18/deploy_steps.md` | Setup and endpoint registration if needed (e.g., POST /artifact/generate) |

### 🧭 Operate
| File Path | Description |
|-----------|-------------|
| `project/docs/user_guide/assemble_artifact.md` | How a GPT or user triggers document generation |
| `project/docs/api_reference/artifact_generation.md` | Input/output spec for planner trigger and REST endpoint |

## 📋 Task Breakdown – WP18

### 🔧 Toolchain Setup
- [ ] Define `assemble_artifact` toolchain steps and intent in `planner_orchestrator.py`
- [ ] Create `assemble_artifact_chain.py` and wire ordered tools

### 🧱 Tool Wrappers
- [ ] `loadSectionMetadata.py` – Query and sort ArtifactSections by gate
- [ ] `formatSection.py` – Apply templates to section content
- [ ] `mergeSections.py` – Combine into single markdown string with headers
- [ ] `finalizeDocument.py` – Add TOC, title, versioning

### 🗂 Storage and Output
- [ ] `commitArtifact.py` – Save final doc and ReasoningTrace
- [ ] Model + create `DocumentVersionLog` table for output metadata

### 🧪 Test
- [ ] Insert sample ArtifactSections for testing
- [ ] Create CLI test script: `test_assemble_artifact.py`
- [ ] Validate output content, trace, versioning

### 📘 Docs
- [ ] Design plan (overview, inputs/outputs, steps)
- [ ] Template reference (structure, naming, dynamic fields)
- [ ] Gate render map (section order per gate)

---

## 🛠️ Recommended: Toolchain for WP18 – `assemble_artifact`

### 📌 Why Use a Toolchain?

Leverages the architecture introduced in WP17b to create a modular, traceable, and GPT-callable document assembly flow:

| Benefit           | Value |
|-------------------|-------|
| 🧩 Modularity      | Break down into manageable, testable steps |
| 📜 Traceability    | Log ReasoningTrace for each phase of assembly |
| 🔁 Reusability     | Rerun with updates or for different gates |
| 🔧 GPT Integration | Planner can trigger toolchain end-to-end |
| 📚 Compliance      | Supports DocumentVersionLog with version and trace linkage |

---

### 🔧 Proposed Toolchain ID
```python
assemble_artifact
[
  "load_section_metadata",  # Fetch from ArtifactSection and gate_reference
  "format_section",         # Apply markdown or template formatting
  "merge_sections",         # Combine ordered section blocks
  "finalize_document"       # Add headers, metadata, TOC, PDF output
]
```
### 📦 Additional Deliverables

- **Toolchain Registration:** Register the `assemble_artifact` toolchain in `planner_orchestrator.py`.
- **Modular Tools:** Implement each toolchain step as a separate tool in `tool_wrappers`.
- **Output Handling:** Save assembled output to:
    - `ArtifactOutput` model (if available), or
    - Git-based markdown file.
- **Traceability:**
    - Log execution trace to `ReasoningTrace`.
    - Create an entry in the new `DocumentVersionLog` model.

### 🗂️ Related Reference Files

- `app/engines/planner_orchestrator.py`
- `project/build/WPs/WP17b/generate_section_chain.py`
- `project/reference/gate_reference_v2.yaml`
- `project/reference/artifact_templates.md` (optional)
- `app/db/models/ArtifactSection.py`
- `app/db/models/ReasoningTrace.py`

### 🔄 Triggering from Planner

The toolchain can be invoked using the following structure:
```json
{ "intent": "assemble_artifact", "artifact_id": "...", "gate_id": 0 }
```
This approach ensures consistency and traceability across content generation and document assembly workflows.

## ✅ Acceptance Criteria
- [ ] Sections assembled in correct order with expected fields
- [ ] Artifacts validated for completeness and accuracy
- [ ] Tools can be called by GPT from planner or confirm-to-draft UX
- [ ] Outputs are previewable by user or other tools
- [ ] Can retrieve all ArtifactSection entries by artifact_id + gate_id
- [ ] Supports multiple versions of the same section and selects latest
- [ ] Assembled artifact logs source ReasoningTrace ids in DocumentVersionLog

### 🔗 Dependencies
- WP16 (Prompt UX, input gathering)
- WP9 (Memory ingestion and structure)
- WP17b (ArtifactSection and chunking and toolchain framework)
- WP20 (Storage and retrieval of artifacts)

**Links:**
- DB schema: `DocumentVersionLog`, `AuditTrail`
- Design: `dense_artifact_generation.md`

### 📥 Inputs
- ArtifactSection entries (queried by artifact_id + gate_id)
- ReasoningTrace metadata (for logging and version trace)
- gate_reference_v2.yaml for ordering and completeness check
- artifact_templates (optional) for formatting output

### 📤 Outputs
- Full markdown or PDF draft
- DocumentVersionLog entry with trace metadata
- Optional preview with chunk references

### 🧠 Notes
- Must handle missing sections or optional fields gracefully
- Allow reuse of templates and alignment to gate definitions
- Keep input/output traceable to gates and sections
- Use DB schemas as source of truth
- Validate artifact completeness against schema early
- Use `ReasoningTrace` to store toolchain step-by-step logs
- Chunk long outputs for traceability and UI interaction
- Validate tool outputs with Pydantic schemas
- Register toolchains + tools cleanly to support planner invocation
- Use `gate_reference.yaml` to drive logic across sections
- Think through output versions: what, why, and how to store