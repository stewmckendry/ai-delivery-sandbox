## 🧩 Work Package Mapping Log

> Phase 1 – Input Mapping (Discovery Files)
> This log is append-only. Each entry maps discovery artifacts to proposed deliverables and work packages. Format:
> - WP ID
> - Deliverables (file paths)
> - Source file reference (path + title/snippet)

---

### 🔹 From `project_goals.md`

**Mapped to WP1 – Policy Artifact Generator**
- `app/templates/gate_document_template.yaml` – from "Project Gating Process" section
- `app/tools/structured_drafter.py` – from "Generate and commit large documents"
- `app/db/models/chain_of_thought.py` – from "Ensure traceability and transparency"
- `app/db/models/validation_checks.py` – from "Add validation tools"
- `app/tools/evidence_prompt.py` – from "Evidence-Based Decision Support"
- `app/tools/raci_scaffold_generator.py` – from "Governance Documentation"
- `app/tools/risk_section_filler.py` – from "Risk, Security, and Privacy Assessments"
- `app/tools/redaction_flagger.py` – from "Political Sensitivities and Cabinet Confidence"
- `app/tools/dual_language_exporter.py` – from "Bilingual Requirements"

**Mapped to WP6 – Review Workflow Routing Layer**
- `app/tools/review_router.py` – from "Interdepartmental Alignment"
- `app/db/models/review_routing_log.py` – from "Interdepartmental Alignment"

**Mapped to WP10 – Export and Translation Layer**
- `app/tools/version_exporter.py` – from "Version Control and Approvals History"
- `app/db/models/approval_signature.py` – from "Version Control and Approvals History"

---

### 🔹 From `policygpt_user_journeys.md`

**Mapped to WP1 – Policy Artifact Generator**
- `app/tools/input_chunker.py` – from Journey A step 4
- `app/tools/section_synthesizer.py` – from Journey A step 4
- `app/tools/outline_drafter.py` – from Journey A step 4
- `app/tools/content_integrator.py` – from Journey A step 7
- `app/tools/preview_renderer.py` – from Journey A step 8
- `app/db/models/project_profile.py` – from Journey A step 4 (metadata coherence)
- `app/tools/yaml_metadata_attacher.py` – from Journey A step 4 (commit with metadata)

**Mapped to WP11 – Document Feedback and Diff Engine**
- `app/tools/feedback_ingester.py` – from Journey C step 1
- `app/tools/section_comparator.py` – from Journey C step 3
- `app/tools/highlight_differ.py` – from Journey C step 3

**Mapped to WP3 – Toolchain Integration Layer**
- `app/engines/section_stitcher.py` – from Journey A step 7
- `app/tools/tool_config_loader.py` – from "Technical Enhancements: Reference Files"

**Mapped to WP8 – Evidence and Citation Tool**
- `app/tools/justification_prompt.py` – from "Evidence-Based Checks"

**Mapped to WP4 – Gating Doc Quality Engine**
- `app/tools/quality_checker.py` – from "Input Guidance" + "Validation Tools"

**Mapped to WP2 – Document Commit + Audit Logging**
- `app/db/models/version_metadata.py` – from "Audit and Metadata"

---

### 🔹 From `PolicyGPT_Features v2.md` and `acceptance_criteria v2.md`

**Mapped to WP1 – Policy Artifact Generator**
- `app/templates/gate_reference/*.yaml` – from Feature 1.1
- `app/templates/artifact_checklists/*.md` – from Acceptance 2.1
- `app/tools/checklist_generator.py`, `validate_artifact.py` – from Feature 1.1

**Mapped to WP2 – Document Commit + Audit Logging**
- `app/tools/commit_to_drive.py`, `commit_document.py` – from Feature 1.2, 2.7
- `app/db/models/version_log.py`, `approval_log.py` – from Acceptance 2.9

**Mapped to WP3 – Toolchain Integration Layer**
- `app/engines/planner_orchestrator.py` – from Feature 2.10
- `app/tools/validate_section.py`, `compose_and_cite.py`, `log_reasoning_trace.py`

**Mapped to WP4 – Gating Doc Quality Engine**
- `app/engines/style_validator.py`, `app/tools/tone_checker.py` – from Feature 2.3, 2.4
- `app/tools/acceptance_criteria_checker.py`

**Mapped to WP6 – Review Workflow Routing Layer**
- `app/tools/feedback_mapper.py`, `app/db/models/comment_log.py` – from Acceptance 2.6

**Mapped to WP7 – Project Profile Engine**
- `app/db/models/project_profile.py`, `profile_editor.py` – from Feature 1.3
- `app/templates/project.yaml`, `app/tools/sync_profile.py`

**Mapped to WP8 – Evidence and Citation Tool**
- `app/tools/evidence_finder.py`, `citation_logger.py` – from Feature 1.4, 2.3
- `app/db/models/evidence_index.py`

**Mapped to WP9 – Input Ingestion + Summarizer**
- `app/tools/file_uploader.py`, `yaml_summarizer.py` – from Feature 2.2
- `app/tools/test/test_ingestion.py`

**Mapped to WP10 – Export and Translation Layer**
- `app/tools/pdf_exporter.py`, `doc_translator.py` – from Acceptance 2.7, 2.8
- `app/tools/test/test_export_translations.py`

**Mapped to WP11 – Document Feedback and Diff Engine**
- `app/tools/diff_checker.py`, `feedback_logger.py` – from Acceptance 2.6

---

## 🧩 Work Package Mapping Log – Part 2

> Continuation of Phase 1 – Input Mapping (System Design Files)
> This log is append-only. Format:
> - WP ID
> - Deliverables (file paths)
> - Source file reference (path + title/snippet)

---

### 🔹 From `system_architecture_v2.md`, `tool_catalog_v2.md`, `api_contracts_v2.md`

**Mapped to WP3 – Toolchain Integration Layer**
- `app/tools/tool_wrappers/compose_and_cite.py` – from tool 1
- `app/tools/tool_wrappers/search_knowledge_base.py` – from tool 2
- `app/tools/tool_wrappers/external_web_search.py` – from tool 3
- `app/tools/tool_wrappers/compose_draft.py` – from tool 4
- `app/tools/tool_wrappers/validate_section.py` – from tool 5
- `app/tools/tool_wrappers/log_reasoning_trace.py` – from tool 6
- `app/tools/tool_wrappers/commit_section.py` – from tool 7
- `app/tools/tool_wrappers/commit_document.py` – from tool 8
- `app/tools/tool_wrappers/fetch_document.py` – from tool 9
- `app/tools/tool_wrappers/get_token_usage.py` – from tool 10
- `app/tools/tool_wrappers/translate_document.py` – from tool 11
- `app/tools/tool_wrappers/query_airtable.py` – from tool 12
- `app/tools/tool_wrappers/parse_transcript.py` – from tool 13
- `app/tools/tool_wrappers/load_corpus.py` – from tool 14
- `app/tools/tool_wrappers/doc_feedback_to_task.py` – from tool 15
- `app/tools/tool_wrappers/diff_and_summarize_sections.py` – from tool 16
- `app/tools/tool_wrappers/submit_document_feedback.py` – from tool 17
- `app/tools/tool_wrappers/summarize_feedback_log.py` – from tool 18

**Mapped to WP11 – Document Feedback and Diff Engine**
- `app/db/models/document_feedback.py` – from "Feedback System"
- `app/db/models/document_diff.py` – from "Feedback System"
- `app/tools/feedback_to_task.py` – from "Feedback System"
- `app/tools/diff_summarizer.py` – from "Feedback System"

**Mapped to WP2 – Document Commit + Audit Logging**
- `app/db/models/approval_log.py` – from "Document Management"
- `app/db/models/document_version_log.py` – from "Document Management"
- `app/db/models/audit_trail.py` – from "Document Management"

---

### 🔹 From `data_flow_master_v2.md`, `db_schema_notes_v2.md`, `session_memory_model_v2.md`

**Mapped to WP3 – Toolchain Integration Layer**
- `app/engines/planner_controller.py` – from Data Flow Stage 1
- `app/engines/memory_sync.py` – from Data Flow Stage 3
- `app/tools/export_controller.py` – from Data Flow Stage 5
- `app/tools/memory_bootstrap.py` – from Memory Model (section: bootstrap from Drive)
- `app/tools/memory_rehydration_logic.py` – from Memory Model (section: rehydrate state)
- `app/tools/yaml_memory_exporter.py` – for `reasoning_trace.yaml`
- `app/tools/yaml_validation_exporter.py` – for `validation_log.yaml`
- `app/tools/yaml_task_trace_exporter.py` – for `planner_task_trace.yaml`

**Mapped to WP11 – Document Feedback and Diff Engine**
- `app/engines/feedback_loop.py` – from Data Flow Stage 4

**Mapped to WP2 – Document Commit + Audit Logging**
- `app/engines/finalizer.py` – from Data Flow Stage 5

**All database models from `db_schema_notes_v2.md` already mapped to appropriate WPs in Part 1**

---

## 🧩 Work Package Mapping Log – Part 3

> Continuation of Phase 1 – Input Mapping (System Design Files)
> This log is append-only. Format:
> - WP ID
> - Deliverables (file paths)
> - Source file reference (path + title/snippet)

---

### 🔹 From `integration_points_v2.md`

**Mapped to WP3 – Toolchain Integration Layer**
- `app/engines/toolchain_middleware.py` – for advanced planner-agent flows
- `app/engines/api_router.py` – for OpenAPI routing across tools and FastAPI
- `app/config/integrations.yaml` – registry for Drive, Airtable, ChromaDB, etc.
- `app/tools/search_knowledge_base.py` – fallback chaining support
- `app/tools/push_commit.py` – for GitHub commit support

**Mapped to WP1 – Policy Artifact Generator**
- `app/templates/final_document_assembler.py` – ensures per-section assembly is token-safe
- `app/tools/session_store.py` – for local YAML snapshots

**Mapped to WP4 – Gating Doc Quality Engine**
- `app/tools/doc_feedback_handler.py` – to add retry/validate on GPT feedback
- `app/db/models/validation_log.py` – supports validation tracking

**Mapped to WP7 – Project Profile Engine**
- `app/db/models/project_profile.py`
- `project/reference/project_profile.yaml` – schema used across flows

**Mapped to WP2 – Document Commit + Audit Logging**
- `app/tools/db_error_exporter.py` – pipeline to extract and format logs

**Mapped to WP5 – System Design Patch**
- `project/build/design_patch/github_integration_notes.md` – tracks optional GitHub integration

> ⚠️ Each integration’s auth flow (OAuth, API Key) is managed via `.env` + Railway env variables

**Secrets and Auth (General Coverage)**
- `.env.sample` – template for all required secrets (Drive, Airtable, OpenAI, etc.)
- `config/env_vars.yaml` – structured mapping of secrets to runtime config

---

### 🔹 From `gate_reference_v2.yaml`, `reference_model_v2.md`, `gating_doc_quality_v2.md`

**Mapped to WP4 – Gating Doc Quality Engine**
- `app/tools/compose_and_cite.py` – chained tool: search > synthesize > draft > validate
- `app/tools/validate_section.py` – quality rule checker before commit
- `app/tools/log_reasoning_trace.py` – saves GPT rationale steps
- `app/engines/document_orchestrator.py` – plans full-document workflow per gate requirements
- `app/db/models/reasoning_trace.py`, `tool_log.py`, `section_draft.py` – structured traceability
- `app/tools/diff_and_summarize_sections.py` – generates reviewer-facing change summaries
- `app/tools/doc_feedback_to_task.py` – feedback parsing for planner reuse
- `app/tools/record_approval_decision.py` – logs reviewer approvals

**Mapped to WP1 – Policy Artifact Generator**
- `app/templates/gate_rationale_prompt_template.md` – embeds structured expectations per section
- `config/policygpt_config.yaml` – system prompt rules and planner toggles

**Mapped to WP11 – Document Feedback and Diff Engine**
- `app/db/models/document_feedback.py`
- `app/db/models/document_diff.py`
- `app/db/models/approval_log.py`

**Mapped to WP3 – Toolchain Integration**
- `app/openapi/openapi_schema.yaml` – adds commit/validate APIs
- `main.py` – routes validator and planner actions

**Mapped to WP5 – System Design Patch**
- `project/build/design_patch/gating_doc_loop_support.md`

**Other Design Tactics**
- `.env.sample`, `config/tool_config.yaml`, `planner_enabled`, `quality_validator` embedded in YAML headers
- `app/tools/chunked_writer.py` – token-safe save/append module
- `app/utils/approval_gatekeeper.py` – checks approval prerequisites
- `app/utils/feedback_flagger.py` – highlights unresolved feedback pre-commit
- `app/utils/consistency_checker.py` – enforces narrative coherence
- `project/reference/gate_reference.yaml` – reused by planner for gate rules

These deliverables operationalize GPT-based quality controls and decision traceability aligned with Canada’s gating requirements.

---

## 🧩 Work Package Mapping Log – Part 4

> Continuation of Phase 1 – Input Mapping (System Design Files)
> This log is append-only. Format:
> - WP ID
> - Deliverables (file paths)
> - Source file reference (path + title/snippet)

---

### 🔹 From `error_handling_matrix_v2.md`

**Mapped to WP3 – Toolchain Integration Layer**
- `app/engines/error_middleware.py` – intercept toolchain errors
- `app/db/models/error_log.py` – database table for structured logging
- `app/db/models/tool_log.py`
- `app/db/models/external_service_log.py`
- `app/db/models/fallback_usage_log.py`
- `app/db/models/task_metadata.py` – expanded to capture retry + error chain

**Mapped to WP4 – Gating Doc Quality Engine**
- `app/tools/validate_section.py` – enriched to trigger retries, enforce OpenAPI scaffold
- `app/utils/retry_handler.py` – manages tool-level retries and backoff

**Mapped to WP2 – Document Commit + Audit Logging**
- `app/db/models/audit_trail.py`
- `app/utils/log_commit_failure.py` – logs failures during Drive commit

**Mapped to WP9 – Input Ingestion + Summarizer**
- `app/tools/structured_input_ingestor.py` – validates uploaded file structure
- `app/tools/retry_ingestion.py` – tracks ingestion failure and retrials

**General Coverage**
- `.env.sample`, `config/tool_config.yaml`, `main.py`, `openapi_schema.yaml` – extended error enums + FastAPI exception logic

> The matrix guides implementation of resilient toolchains, GPT fallback logic, and structured retrials across planner-driven workflows.