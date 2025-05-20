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