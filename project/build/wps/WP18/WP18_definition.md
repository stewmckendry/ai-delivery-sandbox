## WP18 – Artifact Assembly and Routing

### 🎯 Objective
Enable the system to assemble drafted sections into complete artifacts and route them to the correct destinations (e.g., for review, approval, storage). This includes validation, sequencing, and formatting.

### 📦 Scope of Work
**In Scope:**
- Stitch individual `ArtifactSection` entries into full artifacts.
- Log to `DocumentVersionLog`.
- Validate artifact completeness against gate_reference_v2.yaml
- Format output as structured markdown or PDF
- Route outputs to next tools or stages (e.g., feedback, Google Drive storage)
- Build `commitArtifact` and `assembleDraft` tools

**Out of Scope:**
- UI for editing the final draft (handled by future front-end WPs)
- Storage mechanics (WP20)

### 🚀 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/tools/tool_wrappers/assembleDraft.py` | Combines sections into full artifact draft |
| `app/tools/tool_wrappers/commitArtifact.py` | Routes and logs final draft artifact |
| `project/reference/artifact_templates/` | Templates per artifact type |

### ✅ Acceptance Criteria
- [ ] Sections assembled in correct order with expected fields
- [ ] Artifacts validated for completeness and accuracy
- [ ] Tools can be called by GPT from planner or confirm-to-draft UX
- [ ] Outputs are previewable by user or other tools

### 🔗 Dependencies
- WP16 (Prompt UX, input gathering)
- WP9 (Memory ingestion and structure)

**Links:**
- DB schema: `DocumentVersionLog`, `AuditTrail`
- Design: `dense_artifact_generation.md`

### 📥 Inputs
- PromptLog and session memory
- section-level YAML or markdown
- artifact metadata

### 📤 Outputs
- Full artifact draft files
- commit logs with metadata

### 🧠 Notes
- Must handle missing sections or optional fields gracefully
- Allow reuse of templates and alignment to gate definitions