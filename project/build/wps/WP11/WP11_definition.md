## WP ID: WP11
## WP Name: Document Feedback and Diff Engine

### 🌟 Outcome
By the end of this WP, as a **policy drafter**, I will be able to log reviewer feedback, track changes between document versions, and translate feedback into planner tasks. This enhances traceability and supports iterative document refinement.

### 🧽 Scope
**In Scope:**
- Logging structured feedback for any gate document
- Computing diffs between draft versions
- Generating planner tasks based on feedback themes
- Support for both inline and section-level comments

**Out of Scope:**
- Review routing and approvals (covered in WP6)
- Human-in-the-loop interfaces (future UI WP)

### 📦 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/tools/feedback_logger.py` | Logs reviewer comments and feedback context |
| `app/tools/feedback_to_task.py` | Converts feedback into actionable planner tasks |
| `app/tools/diff_summarizer.py` | Compares two document versions to summarize changes |
| `app/db/models/DocumentFeedback.py` | Stores feedback entries with metadata |
| `app/db/models/DocumentDiff.py` | Captures diffs between document versions |
| `app/tools/test/test_feedback_and_diff.py` | Tests feedback logging and diff generation logic |

### 📄 Supporting Documentation (to generate)
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WP11/WP11_feedback_flow.md` | Diagram of feedback collection and processing flow |
| `project/build/wps/WP11/WP11_diff_engine_logic.md` | Spec of how changes are detected and summarized |

### ✅ Acceptance Criteria
- [ ] Feedback can be submitted and logged for any draft section
- [ ] Diffs correctly identify insertions, deletions, and updates
- [ ] Planner can consume `feedback_to_task.py` outputs as new tasks
- [ ] Diff logs and feedback entries are queryable for audit

### 💠 Tasks
| Task ID | Description |
|---------|-------------|
| T1 | Build logger to capture structured feedback from reviewers |
| T2 | Build diff summarizer for comparing draft versions |
| T3 | Translate feedback themes into planner-compatible tasks |
| T4 | Create DB models to persist diffs and feedback logs |
| T5 | Write integration tests for full logging and diffing flow |

### 📚 Reference Documentation
| File Path | Usage |
|-----------|--------|
| `gate_reference_v2.yaml` | For linking feedback to specific gate sections |
| `acceptance_criteria_v2.md` | For validation rules impacted by feedback |
| `session_memory_model_v2.md` | For storing feedback in mid-term memory |

### 📝 Notes to Development Team
- Must link feedback to versioned document IDs
- Feedback may come from multiple reviewers; track source
- Must support planner hook to enable iterative improvement

### 🧠 Clarifications
- 🌟 **Feedback-to-task linkage:** `feedback_to_task.py` bridges reviewer comments to planner task input format (used in WP3a).
- 📌 **Diff engine supports:** human-readable summaries for UI display, as well as machine-parsable logs for traceability.
- ⚖️ **Integration timing:** Feedback gets translated into planner updates during ongoing session (WP3a); may also trigger section reruns (WP1b).
