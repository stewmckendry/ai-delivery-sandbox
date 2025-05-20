## 🧭 Traceability Matrix – Part 1

This matrix maps every element from discovery and system design to its corresponding work package (WP). Each row shows one deliverable, tagged with the source reference and WP.

## Discovery → Work Packages
| Source File | Deliverable | Work Package |
|-------------|-------------|--------------|
| policygpt_user_journeys.md | Journey A - Plan a Gate Document | WP1a, WP1b |
| policygpt_user_journeys.md | Journey B - Collaborate and Iterate | WP2, WP6, WP11 |
| policygpt_user_journeys.md | Journey C - Finalize and Export | WP10 |
| project_goals.md | Complete gate-ready documents | All |

## PolicyGPT_Features v2.md
| Feature | Deliverable | Work Package |
|---------|-------------|--------------|
| Structured drafting | `app/tools/structured_drafter.py` | WP1a |
| Redaction pass | `app/tools/redaction_flagger.py` | WP1a |
| Gate templates | `app/templates/gate_document_template.yaml` | WP1a |
| Section tasking & progress | `app/tools/task_status_tracker.py` | WP1b |
| Approval flow & signoff | `app/tools/review_router.py`, `app/db/models/approval_signature.py` | WP6 |
| Commit to project | `app/tools/push_commit.py` | WP2 |
| Document diff + summarizer | `app/tools/diff_summarizer.py` | WP11 |
| Metadata YAML attachment | `app/tools/yaml_metadata_attacher.py` | WP2 |
| Export gate packages | `app/tools/export_to_gate_package.py` | WP10 |
| Validate against reference | `app/tools/validate_section.py` | WP4 |
| Feedback application | `app/tools/feedback_to_task.py` | WP11 |
| Evidence prompt integration | `app/tools/evidence_prompt.py`, `app/tools/evidence_logger.py` | WP8 |
| Session Memory & Rewind | `app/db/models/PromptLog.py`, `app/db/models/SessionSnapshot.py` | WP3a |
| System logging | `app/db/models/ToolLog.py`, `app/db/models/ErrorLog.py` | WP3c |

## acceptance_criteria v2.md
| Acceptance Criteria | Deliverable | Work Package |
|---------------------|-------------|--------------|
| User can draft structured sections | `app/tools/structured_drafter.py` | WP1a |
| Metadata validation is automated | `app/tools/yaml_metadata_attacher.py` | WP2 |
| Reviewer routing is based on section type | `app/tools/review_router.py`, `app/engines/reviewer_router.py` | WP6 |
| Commit metadata is attached | `app/tools/push_commit.py` | WP2 |
| Feedback is applied via GPT or link | `app/tools/feedback_to_task.py` | WP11 |
| Exported packages match gate template | `app/tools/export_to_gate_package.py` | WP10 |
| Language access is integrated | `app/tools/dual_language_exporter.py` | WP10 |
| All tool use is logged | `app/db/models/ToolLog.py`, `app/engines/toolchain_middleware.py` | WP3c |
| System restores memory on session resume | `app/db/models/SessionSnapshot.py`, `app/engines/memory_sync.py` | WP3a |