# 📦 Work Package Overview – Consolidated Mapping

## Section A: Deliverables by Work Package

### WP1a – Scaffolding + Assembly

* `app/templates/final_document_assembler.py`
* `app/tools/gate_section_scaffolder.py`
* `app/tools/gate_section_expander.py`

### WP1b – Task Logging + Finalization

* `app/tools/gate_section_finalizer.py`
* `app/tools/tasklog_updater.py`
* `app/tools/session_store.py`
* `app/db/models/ArtifactSection.py`

### WP2 – Document Commit + Audit Logging

* `app/db/models/DocumentVersionLog.py`
* `app/db/models/AuditTrail.py`
* `app/db/models/ApprovalLog.py`
* `app/tools/db_error_exporter.py`
* `app/utils/log_commit_failure.py`
* `app/db/schema_migrations.sql`

### WP3a – Planner + Memory Layer

* `app/engines/planner_orchestrator.py`
* `app/engines/memory_sync.py`
* `app/db/models/PromptLog.py`
* `app/db/models/SessionSnapshot.py`

### WP3b – Tool Registration + API Wrapping

* `app/tools/tool_registry.py`
* `app/tools/tool_wrappers/*.py`
* `app/engines/api_router.py`
* `main.py`
* `app/openapi/openapi_schema.yaml`
* `config/tool_config.yaml`
* `config/integrations.yaml`

### WP3c – Middleware + Logging

* `app/engines/error_middleware.py`
* `app/engines/toolchain_middleware.py`
* `app/tools/search_knowledge_base.py`
* `app/tools/push_commit.py`
* `app/db/models/ErrorLog.py`
* `app/db/models/ToolLog.py`
* `app/db/models/ExternalServiceLog.py`
* `app/db/models/FallbackUsageLog.py`
* `.env.sample`

### WP4 – Gating Doc Quality Engine

* `app/tools/validate_section.py`
* `app/tools/doc_feedback_handler.py`
* `app/utils/retry_handler.py`
* `app/db/models/ValidationLog.py`

### WP5 – System Design Patch + Harmonization

* Focused on consolidating all design insights from implementation prior to build kickoff
* Resolves overlapping definitions across discovery and system design
* Examples: merging fields between `tool_catalog_v2.md` and `api_contracts_v2.md`
* Deliver: `project/build/design_patch/github_integration_notes.md`, updated `tool_catalog_v2.md`, `session_memory_model_v2.md`

### WP6 – Review Workflow Routing Layer

* `app/engines/reviewer_router.py`
* `app/db/models/ReviewAssignment.py`
* `app/tools/test/test_routing.py`

### WP7 – Project Profile Engine

* `app/db/models/ProjectProfile.py`
* `project/reference/project_profile.yaml`

### WP8 – Evidence and Citation Tool

* `app/tools/citation_inserter.py`
* `app/tools/evidence_lookup.py`
* `app/tools/evidence_logger.py`
* `app/tools/generate_citation_index.py`
* `app/db/models/EvidenceCitation.py`
* `app/db/models/CitationSource.py`
* `app/db/models/EvidenceIndex.py`

### WP9 – Input Ingestion + Summarizer

* `app/tools/structured_input_ingestor.py`
* `app/tools/retry_ingestion.py`
* `app/tools/text_extractor.py`

### WP10 – Export and Translation Layer

* `app/tools/export_to_gate_package.py`
* `app/tools/translate_to_official_language.py`

### WP11 – Document Feedback and Diff Engine

* `app/tools/feedback_logger.py`
* `app/tools/feedback_to_task.py`
* `app/tools/diff_summarizer.py`
* `app/db/models/DocumentFeedback.py`
* `app/db/models/DocumentDiff.py`
* `app/tools/test/test_feedback_and_diff.py`

### WP12 – System Design Feedback Loop

* Captures mismatches between implementation and spec during build
* Provides real-time design updates to improve system documentation
* Examples: updating OpenAPI spec to reflect discovered fallback behavior
* Deliver: `project/system_design/design_patch_*.md`

---

## 🧪 Identified Issues and Recommendations (Applied)

### 🔁 Deduplication + Naming Cleanup

* `AuditTrail.py` scoped to WP2 only
* `tasklog_updater.py` renamed to `task_status_tracker.py`
* Ensured consistent naming for logs and models

### 🔧 Optimization Strategy

* Split overloaded WP1 and WP3 for better focus and parallelism
* New WP12 introduced for design reflection + feedback updates

---

## 🌀 Iteration + Sequencing

Each phase includes a user-focused milestone for measurable value delivery:

### ✅ Phase 1 – MVP Focus (Parallel)

**As a policy drafter**, I will be able to scaffold, ingest, and assemble draft gate documents using input material. This allows me to produce an initial version of required documentation without manual formatting or duplication.

* WP1a: Scaffolding + Assembly
* WP3a: Planner + Memory Layer
* WP3b: Tool Wrapping + API
* WP9: Input Ingestion

### ⏩ Phase 2 – Iterative Enhancements (Parallel)

**As a policy team**, we can now validate document quality, track version differences, and cite evidence. This improves quality, accuracy, and auditability of the draft documents.

* WP1b: Logging + Finalization
* WP3c: Middleware + Logging
* WP4: Gating Doc Quality
* WP8: Citation Tool
* WP11: Feedback + Diff Engine

### 🔁 Phase 3 – Workflow Completion (Some Sequential)

**As a review committee**, I can receive documents for review, route them to appropriate approvers, export official versions, and store project profiles. This enables full lifecycle management of policy submissions.

* WP2: Commit + Logging
* WP6: Review Routing
* WP10: Export + Translate
* WP7: Project Profile

### 🔄 Always Active

* WP12: System Design Feedback – provides real-time design updates during build
* WP5: Harmonization + Docs – ensures consistent updates across documentation

---

## ✅ Next

Proceed to traceability matrix (source → WP coverage), then commit final file