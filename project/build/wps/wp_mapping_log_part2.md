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