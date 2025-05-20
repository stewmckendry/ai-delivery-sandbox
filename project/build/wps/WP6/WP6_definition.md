## WP ID: WP6  
## WP Name: Review Workflow Routing Layer

### 🌟 Outcome
By the end of this WP, as a **review committee coordinator**, I will be able to automatically route drafted documents to appropriate reviewers based on defined rules and project profiles. This enables faster and more organized policy review cycles.

### 🯽 Scope

**In Scope:**
- Logic for assigning reviewers to specific gate sections or artifacts
- Modeling reviewer assignments in the database
- Basic test coverage for routing logic

**Out of Scope:**
- Review interface for reviewers (covered in future WPs)
- Commenting or inline review workflows (covered elsewhere)

### 📦 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/engines/reviewer_router.py` | Core routing engine assigning reviewers to artifacts |
| `app/db/models/ReviewAssignment.py` | DB model capturing who is assigned to review what |
| `app/tools/test/test_routing.py` | Test file validating routing behavior and edge cases |

### 📄 Supporting Documentation (to generate)
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WP6/WP6_routing_rules.md` | Describes logic and rules for routing decisions |
| `project/build/wps/WP6/WP6_test_coverage_plan.md` | Explains test approach and edge cases for reviewer routing |

### ✅ Acceptance Criteria
- [ ] Reviewer router assigns reviewers per configuration and section type
- [ ] All reviewer assignments are logged in `ReviewAssignment` model
- [ ] Routing logic is covered by automated tests
- [ ] Documentation written for routing rules and test coverage

### 🛠 Tasks
| Task ID | Description |
|---------|-------------|
| T1 | Implement `reviewer_router.py` with config-driven logic |
| T2 | Define and create `ReviewAssignment` DB model |
| T3 | Write test cases for routing engine |
| T4 | Write routing rule doc for maintainability |
| T5 | Draft test coverage plan for QA transparency |

### 📚 Reference Documentation
| File Path | Usage |
|-----------|--------|
| `project_goals.md` | Emphasizes routing for structured review |
| `acceptance_criteria_v2.md` | Defines review completion as part of document lifecycle |
| `tool_catalog_v2.md` | Contains some mention of review role routing behavior |

### 📝 Notes to Development Team
- Keep logic modular so it can expand for multiple reviewer types
- Start with hardcoded routing if needed, then transition to config-based
- Ensure traceability of reviewer assignments for audit purposes