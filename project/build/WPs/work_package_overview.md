## 🧱 Work Package Overview

This document provides a consolidated mapping of all deliverables, organized by work package (WP), and includes a transposed traceability matrix to verify alignment with source discovery and system design documentation.

---

### 🧩 Work Packages Summary

#### WP1a – Structured Drafting Tools
- `app/tools/structured_drafter.py`
- `app/tools/redaction_flagger.py`
- `app/templates/gate_document_template.yaml`
- `app/tools/section_synthesizer.py`

#### WP1b – Section Progress Tracking
- `app/tools/task_status_tracker.py`
- `app/db/models/PromptLog.py`

#### WP2 – Commit + Metadata + Versions
- `app/tools/push_commit.py`
- `app/tools/yaml_metadata_attacher.py`
- `app/db/models/DocumentVersionLog.py`
- `app/db/models/AuditTrail.py`
- `app/db/models/approval_signature.py`

#### WP3a – Session Memory Engine
- `app/engines/planner_orchestrator.py`
- `app/db/models/SessionSnapshot.py`
- `app/db/models/PromptLog.py`
- `app/engines/memory_sync.py`

#### WP3b – Tool Dispatch + Routing
- `app/engines/api_router.py`
- `app/tools/tool_wrappers/*.py`

#### WP3c – Middleware + Logging + Errors
- `app/engines/toolchain_middleware.py`
- `app/engines/error_middleware.py`
- `app/db/models/ToolLog.py`
- `app/db/models/ErrorLog.py`

#### WP4 – Validation Engine
- `app/tools/validate_section.py`
- `app/db/models/validation_checks.py`

#### WP5 – System Design Feedback (Dynamic)
- `project/system_design/*.md` updates

#### WP6 – Review + Approvals
- `app/tools/review_router.py`
- `app/engines/reviewer_router.py`
- `app/db/models/ReviewAssignment.py`

#### WP7 – Metadata Model
- `app/db/models/project_profile.py`

#### WP8 – Evidence Tools
- `app/tools/evidence_prompt.py`
- `app/tools/evidence_logger.py`
- `app/db/models/EvidenceIndex.py`

#### WP10 – Exporters
- `app/tools/export_to_gate_package.py`
- `app/tools/dual_language_exporter.py`

#### WP11 – Feedback + Diff Tools
- `app/tools/feedback_to_task.py`
- `app/tools/diff_summarizer.py`
- `app/db/models/DocumentDiff.py`
- `app/db/models/DocumentFeedback.py`

#### WP12 – Design Artifacts Cleanup
- `project/system_design/*.md` updates post-review

---

### 🔁 Iteration & Sequencing

**Phase 1 – MVP (Fast Iteration)**
- WP1a, WP1b, WP2, WP3a → “As a policy drafter, I will be able to structure and save content with memory and metadata, allowing me to collaborate with early signal fidelity.”

**Phase 2 – Add Collaboration + Quality Tools**
- WP3b, WP3c, WP4, WP6, WP11

**Phase 3 – Finish Line**
- WP7, WP8, WP10 → enables export, evidence and compliance

**Meta Packages**
- WP5 runs continuously for design feedback
- WP12 is a scoped sweep for systemic artifact alignment

Refer to the traceability matrices for alignment with source materials.
