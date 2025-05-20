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