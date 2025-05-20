## WP ID: WP1b
## WP Name: Task Logging + Finalization

### 🌟 Outcome
By the end of this WP, as a **policy drafter**, I will be able to finalize drafted sections and persist them to the canonical record, while capturing traceable task execution steps. This supports **document versioning**, **traceability**, and **future rehydration of context**.

### 🧽 Scope
**In Scope:**
- Finalizing and locking completed gate sections
- Persisting finalized content to session memory DB (`ArtifactSection`)
- Capturing reasoning trace for the section
- Logging task completion to the session

**Out of Scope:**
- Document validation or evidence tagging (WP4, WP8)
- Full session snapshot or audit trail across artifacts (WP2)
- Long-term memory commit (e.g. Google Drive)

### 📦 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/tools/gate_section_finalizer.py` | Marks a gate section as complete, triggers logging of final content and reasoning. |
| `app/tools/tasklog_updater.py` | Logs task progress and transitions in session memory. |
| `app/tools/session_store.py` | Persists finalized section, stores memory traces for planner rehydration. |
| `app/db/models/ArtifactSection.py` | DB model for storing canonical section content with metadata. |

### 📄 Supporting Documentation (to generate)
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WP1b/WP1b_design.md` | Design logic for finalization and memory writes. |
| `project/build/wps/WP1b/WP1b_deployment.md` | Deployment and testing instructions. |
| `project/build/wps/WP1b/WP1b_tests.md` | Test coverage plan. |

### ✅ Acceptance Criteria
- [ ] Finalizer locks section and updates memory state.
- [ ] Reasoning trace is persisted alongside content.
- [ ] Task logger reflects section finalization.
- [ ] DB model `ArtifactSection` is active and stores content.
- [ ] Modules deployed to dev and pass unit + integration tests.

### 🛠 Tasks
| Task ID | Description |
|---------|-------------|
| T1 | Implement `ArtifactSection.py` model |
| T2 | Implement `session_store.py` for mid-term memory writes |
| T3 | Implement `tasklog_updater.py` to capture section task states |
| T4 | Implement `gate_section_finalizer.py` logic to close and log section |
| T5 | Write tests for finalizer + store modules |
| T6 | Deploy to dev and validate with WP1a output |

### 📚 Reference Documentation
| File Path | Usage |
|-----------|--------|
| `policygpt_user_journeys.md` | Finalization checkpoints per gate section |
| `PolicyGPT_Features v2.md` | Task traceability and section locking features |
| `acceptance_criteria v2.md` | Confirmation criteria for final section status |
| `session_memory_model_v2.md` | Memory model (focus on mid-term memory and `ArtifactSection`) |
| `tool_catalog_v2.md` | Tool registration and task handler expectations |

### 📝 Notes to Development Team
- Finalized section content must be preserved for planner rehydration.
- Reasoning traces should follow naming schema (`reasoning_trace.yaml`).
- `tasklog_updater.py` should be extensible to future task states.

---

### 🔍 Clarification Notes

**Session Memory Model:**
- WP1b builds **Mid-Term Memory**: YAML + DB persistence (e.g., `ArtifactSection`, `reasoning_trace.yaml`)
- Does *not* handle **Short-Term Memory** (runtime-only) or **Long-Term Memory** (Google Drive)

**Google Drive Commit:**
- Covered in **WP2 – Commit + Logging**

**Quality Checks:**
- Automated validation → **WP4**
- Human feedback + diffing → **WP11**

**User Interactions:**
- Uploading inputs → **WP9**
- Draft feedback → **WP11**