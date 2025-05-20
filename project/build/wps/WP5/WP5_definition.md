## WP ID: WP5
## WP Name: System Design Patch + Harmonization

### 🌟 Outcome
By the end of this WP, as a **design steward**, I will be able to merge, harmonize, and patch system design documentation across all discovery and implementation sources. This ensures alignment and clarity before and during development.

### 🧽 Scope
**In Scope:**
- Reconciliation of overlapping fields and tool definitions across discovery documents
- Updating source of truth documents (`tool_catalog_v2.md`, `session_memory_model_v2.md`)
- Capturing integration notes and observed mismatches
- Reflecting real implementation paths back into design (e.g., handling fallback behavior)

**Out of Scope:**
- Tool implementation or runtime integration (covered by other WPs)
- Planning or work package structure changes (handled in planning phase)

### 📦 Deliverables
| File Path | Description |
|-----------|-------------|
| `project/build/design_patch/github_integration_notes.md` | Captures how GitHub is used to track builds, traceability, logs, and commits in this project. Reflects project build infra. |
| `tool_catalog_v2.md` (updated) | Harmonized list of tools, owners, scopes, categories, and API paths. |
| `session_memory_model_v2.md` (updated) | Updated to reflect what memory models are implemented vs. placeholders. |

### 📄 Supporting Documentation (to generate)
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WP5/WP5_field_merge_notes.md` | Matrix mapping overlapping fields across specs with final resolved schema. |
| `project/build/wps/WP5/WP5_source_truth_decisions.md` | Decisions on which document becomes source of truth for each spec type (tools, APIs, memory). |

### ✅ Acceptance Criteria
- [ ] All tool specs de-duplicated and unified across `tool_catalog_v2.md`, `api_contracts_v2.md`
- [ ] Memory model scope clarified and updated
- [ ] GitHub usage documented for this project's delivery infra
- [ ] Gaps logged for future system design patches (e.g., fallback)

### 💠 Tasks
| Task ID | Description |
|---------|-------------|
| T1 | Audit overlapping tool and API fields |
| T2 | Update `tool_catalog_v2.md` and resolve conflicts |
| T3 | Patch `session_memory_model_v2.md` with implemented scope |
| T4 | Write integration notes on GitHub usage (project-side) |
| T5 | Document decisions on source of truth documents |

### 📚 Reference Documentation
| File Path | Usage |
|-----------|--------|
| `tool_catalog_v2.md` | Tool attributes and metadata |
| `api_contracts_v2.md` | Tool contract formats and methods |
| `session_memory_model_v2.md` | Memory layering logic |
| `system_architecture_v2.md` | High-level component relationships |

### 📝 Notes to Development Team
- Ensure no changes are lost from original mappings.
- Log tradeoffs and mismatches for downstream updates.
- Clarify which components are MVP vs. future.

### 🧠 Clarifications
- 🔁 This WP focuses on the **system design as built by the team**. It’s a reflection loop from implementation back to design.
- 📘 GitHub integration here refers to how we are using GitHub in the **project** (e.g., commits, traceability, logs). It is **not** yet used in the PolicyGPT runtime architecture.
- 🧪 Future runtime GitHub integration will be tracked in WP15.