## WP ID: WP7
## WP Name: Project Profile Engine

### 🌟 Outcome
By the end of this WP, as a **policy drafter or approver**, I will be able to define, update, and retrieve the active project profile that informs how PolicyGPT operates. This profile will evolve dynamically with user inputs and system outputs to ensure tailored document generation.

### 🧽 Scope
**In Scope:**
- Creating and persisting a `ProjectProfile` model
- Initializing `project_profile.yaml` as a template for project settings
- Dynamically updating the `project_profile` in memory during sessions
- Using profile fields to guide generation and validation logic
- Exposing the profile to users via a `showProfile` tool
- Automatically updating profile as part of the background tool chaining process

**Out of Scope:**
- User-facing UI to edit the profile (covered in future UI WPs)
- Full lifecycle audit of changes (handled in logging WPs)

### 📦 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/db/models/ProjectProfile.py` | SQLAlchemy model for storing project-level settings |
| `project/reference/project_profile.yaml` | YAML template and source of truth for a project's configuration |
| `app/tools/show_profile.py` | Tool that returns the current active project profile in memory |
| `app/tools/project_profile_updater.py` | Background logic to update the project profile dynamically during tool execution |

### 📄 Supporting Documentation (to generate)
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WP7/WP7_profile_fields_reference.md` | Table describing all fields in the project profile and their uses |
| `project/build/wps/WP7/WP7_runtime_profile_flow.md` | Diagram and flow of how the profile is updated dynamically in sessions |

### ✅ Acceptance Criteria
- [ ] A `ProjectProfile` object is initialized and persisted for each project
- [ ] YAML reference can be loaded and edited
- [ ] Updates to the profile occur automatically in memory during session execution
- [ ] The profile influences scaffolding, drafting, and validation
- [ ] Users can run `showProfile` to inspect project configuration

### 💪 Tasks
| Task ID | Description |
|---------|-------------|
| T1 | Define SQLAlchemy `ProjectProfile` schema |
| T2 | Create initial YAML schema and default config |
| T3 | Build `project_profile_updater.py` for runtime updates |
| T4 | Implement `show_profile.py` tool for user access |
| T5 | Add hooks in planner to update profile during tool chaining |
| T6 | Validate profile values are being consumed by key tools |

### 📚 Reference Documentation
| File Path | Usage |
|-----------|--------|
| `policygpt_user_journeys.md` | Identifies key user-configurable items |
| `acceptance_criteria_v2.md` | References to dynamic fields and scaffolding needs |
| `system_architecture_v2.md` | Shows planner/memory profile injection points |

### 📝 Notes to Development Team
- Profile values will influence gate detection, document generation, and quality checks.
- Treat the profile as an evolving state: not static YAML, but a live config context.
- Must persist between sessions and reload on reconnect.

### 🧠 Clarifications
- 🧠 The profile is updated as part of the **toolchain planner execution** – tools can write metadata back to the profile.
- 🔄 While the YAML file seeds the profile, live updates occur in memory and in the DB.
- 👁 Users can inspect it at any time via the `showProfile` tool.