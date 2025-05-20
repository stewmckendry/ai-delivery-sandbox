# 🛍 Traceability Matrix – Part 2

Continuing from Part 1, this matrix maps remaining items from system design and discovery documents to relevant work packages.

## api_contracts_v2.md (continued)
| Contract | Deliverable | Work Package |
|----------|-------------|--------------|
| PUT /validate_section | `app/tools/validate_section.py` | WP4 |
| GET /diff_summary | `app/tools/diff_summarizer.py` | WP11 |
| GET /export_doc | `app/tools/export_to_gate_package.py` | WP10 |

## data_flow_master_v2.md
| Flow Node | Deliverable | Work Package |
|-----------|-------------|--------------|
| Planner → Tool Dispatcher | `app/engines/planner_orchestrator.py`, `app/engines/api_router.py` | WP3a / WP3b |
| Tool Dispatcher → Tool Wrappers | `app/tools/tool_wrappers/*.py` | WP3b |
| Tool Wrappers → Middleware → Logging | `app/engines/toolchain_middleware.py`, `app/db/models/ToolLog.py` | WP3c |
| Middleware → Session Memory Sync | `app/engines/memory_sync.py`, `app/db/models/SessionSnapshot.py` | WP3a |

## db_schema_notes_v2.md
| Table | Deliverable | Work Package |
|-------|-------------|--------------|
| DocumentVersionLog | `app/db/models/DocumentVersionLog.py` | WP2 |
| AuditTrail | `app/db/models/AuditTrail.py` | WP2 |
| ReviewAssignment | `app/db/models/ReviewAssignment.py` | WP6 |
| FeedbackLog | `app/db/models/DocumentFeedback.py` | WP11 |
| DiffSummary | `app/db/models/DocumentDiff.py` | WP11 |
| ToolLog, ErrorLog | `app/db/models/ToolLog.py`, `app/db/models/ErrorLog.py` | WP3c |
| EvidenceIndex | `app/db/models/EvidenceIndex.py` | WP8 |

## session_memory_model_v2.md
| Element | Deliverable | Work Package |
|---------|-------------|--------------|
| Prompt History | `app/db/models/PromptLog.py` | WP3a |
| Memory Snapshots | `app/db/models/SessionSnapshot.py` | WP3a |
| Task Logs | `app/tools/task_status_tracker.py` | WP1b |

## integration_points_v2.md
| Integration Point | Deliverable | Work Package |
|------------------|-------------|--------------|
| External Feedback | `app/tools/feedback_to_task.py` | WP11 |
| GPT/Tool Split | `app/engines/planner_orchestrator.py` | WP3a |
| Commit/Metadata | `app/tools/push_commit.py`, `app/tools/yaml_metadata_attacher.py` | WP2 |
| Redaction Pass | `app/tools/redaction_flagger.py` | WP1a |
| Validate Against Reference | `app/tools/validate_section.py` | WP4 |

## reference_model_v2.md
| Model Element | Deliverable | Work Package |
|---------------|-------------|--------------|
| Reference-Driven Generation | `app/tools/structured_drafter.py`, `app/tools/section_synthesizer.py` | WP1a |
| Quality Framework | `app/tools/validate_section.py`, `app/db/models/validation_checks.py` | WP4 |
| Role-Specific Review | `app/tools/review_router.py`, `app/engines/reviewer_router.py` | WP6 |

## gate_reference_v2.yaml
| Reference Gate | Deliverable | Work Package |
|----------------|-------------|--------------|
| Gate Templates | `app/templates/gate_document_template.yaml` | WP1a |
| Required Metadata | `app/db/models/project_profile.py` | WP7 |
| Reviewer Signature Requirements | `app/db/models/approval_signature.py` | WP2 |

## gating_doc_quality_v2.md
| Quality Dimension | Deliverable | Work Package |
|------------------|-------------|--------------|
| Internal Consistency | `app/tools/validate_section.py` | WP4 |
| Evidence-Based Argument | `app/tools/evidence_logger.py`, `app/tools/evidence_prompt.py` | WP8 |
| Accessibility & Language | `app/tools/dual_language_exporter.py` | WP10 |
| Metadata Compliance | `app/tools/yaml_metadata_attacher.py` | WP2 |

## error_handling_matrix_v2.md
| Error Type | Deliverable | Work Package |
|------------|-------------|--------------|
| Tool Execution Failures | `app/engines/error_middleware.py` | WP3c |
| Validation Failures | `app/tools/validate_section.py` | WP4 |
| Feedback Application Errors | `app/tools/feedback_to_task.py` | WP11 |
| Export/Import Errors | `app/tools/export_to_gate_package.py` | WP10 |