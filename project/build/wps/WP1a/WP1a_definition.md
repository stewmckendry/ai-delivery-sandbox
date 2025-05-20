## WP ID: WP1a
## WP Name: Scaffolding + Assembly

### 🌟 Outcome
By the end of this WP, as a **policy drafter**, I will be able to scaffold structured gate sections from ingested source materials and assemble them into a coherent draft gate document. This supports the benefit of **accelerated document creation**, **consistency across gates**, and **reduction in manual formatting work**.

### 🧽 Scope
**In Scope:**
- Logic to interpret inputs and generate draft gate sections.
- Assembly engine to stitch multiple sections into final document layout.
- Use of `gate_reference.yaml` to align scaffold structure to gate expectations.
- Modular and testable tool implementations.

**Out of Scope:**
- Citation insertion or evidence validation (handled in WP8).
- Final review routing (WP6).
- Export and translation (WP10).

### 📦 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/templates/final_document_assembler.py` | Assembles scaffolded gate sections into a full draft gate document, based on section priority/order. |
| `app/tools/gate_section_scaffolder.py` | Generates the initial section layout with placeholder scaffolding for each gate based on project profile, input material, and `gate_reference.yaml`. |
| `app/tools/gate_section_expander.py` | Uses planning logic to expand scaffolds into detailed content using context memory. |

### 📄 Supporting Documentation (to generate)
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WP1a/WP1a_design.md` | Design logic for scaffolding and document assembly. |
| `project/build/wps/WP1a/WP1a_deployment.md` | Steps to deploy and verify scaffolding tools in dev/test. |
| `project/build/wps/WP1a/WP1a_tests.md` | Unit and integration test cases. |

### ✅ Acceptance Criteria
- [ ] Scaffolder reads `gate_reference.yaml` to scaffold correct sections.
- [ ] Outputs structurally complete gate sections with correct placeholders.
- [ ] Expander fills in placeholder content based on memory planning.
- [ ] Assembler constructs a valid full draft document.
- [ ] Modules are testable in isolation and integrated in dev environment.

### 💪 Tasks
| Task ID | Description |
|---------|-------------|
| T1 | Review memory and planner logic for expansion inputs |
| T2 | Parse `gate_reference.yaml` in scaffolder |
| T3 | Implement `gate_section_scaffolder.py` |
| T4 | Implement `gate_section_expander.py` |
| T5 | Implement `final_document_assembler.py` |
| T6 | Write unit tests for all modules |
| T7 | Deploy to dev and test with sample inputs |

### 📚 Reference Documentation
| File Path | Usage |
|-----------|--------|
| `policygpt_user_journeys.md` | Drafting flow and section scaffolding expectations |
| `PolicyGPT_Features v2.md` | Features related to section creation |
| `acceptance_criteria v2.md` | Completeness and quality metrics for draft output |
| `system_architecture_v2.md` | Assembler interface and memory interaction |
| `session_memory_model_v2.md` | Context handling for section expansion |
| `gate_reference_v2.yaml` | Defines required artifacts and outlines per gate |

### 📝 Notes to Development Team
- Ensure scaffolder supports variable section ordering.
- Expander should call planner outputs and allow retries.
- Use mock inputs to validate assembler logic with partial sections.
- Scaffolder must validate compliance with artifact outline in `gate_reference.yaml`.