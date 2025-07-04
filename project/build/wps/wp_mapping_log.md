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

### 🔹 From `system_architecture_v2.md` + `tool_catalog_v2.md` + `api_contracts_v2.md`

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
- `app/db/models/document_feedback.py`, `app/db/models/document_diff.py`, `app/tools/feedback_to_task.py`, `app/tools/diff_summarizer.py` – from "Feedback System" layer

**Mapped to WP2 – Document Commit + Audit Logging**
- `app/db/models/approval_log.py`, `document_version_log.py`, `audit_trail.py` – from "Feedback System" + "Document Management" layers

✅ More mappings to be appended as remaining system_design files are processed.
