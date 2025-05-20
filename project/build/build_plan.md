## Work Packages (Expanded)

---

### WP1. System Scaffolding and API Skeleton

**Outcome**: Base FastAPI app and project structure

**Scope**:
- `FastAPI App Init`: Create `main.py`, load routers, set logging.
- `Router Layout`: Base routers folder structure, include route loader.
- `Exception Handling`: Centralize error types and responses.
- `Dev Environment`: Include `.env`, pre-commit hooks, local run scripts.

**Tasks**:
- [ ] Create `main.py` with health check route.
- [ ] Setup `routers/`, `services/`, `models/`, `logs/` folders.
- [ ] Implement error response model.
- [ ] Add CORS, logging, and JSON config middleware.
- [ ] Add `run-local.sh` and update `requirements.txt`.
- [ ] Write unit test for health route.

**Acceptance Criteria**:
- [ ] `uvicorn main:app` runs without error.
- [ ] `/health` returns OK JSON.
- [ ] Lint and test pass locally.
- [ ] Dev can scaffold new routers without rework.

**📂 Related System Design References**
- system_architecture.md
- "The FastAPI app exposes a toolchain-based API under /tasks/*, with tool dispatch, memory access, and reasoning trace logging split into logical modules."
- api_contracts.md
- "Defines POST /tasks/commit_and_log_output, GET /memory/fetch and tool execution routes (/tools/execute, etc.)."
- error_handling_matrix.md
- "All APIs must return a JSON error payload with keys: error_type, message, trace_id if present."

---

### WP2. Database Models and Schema Integration

**Outcome**: Working DB layer with Alembic migrations.

**Scope**:
- `Model Definitions`: SQLAlchemy models for all entities (session, trace, feedback, etc.).
- `Migration Tooling`: Alembic setup with autogen and versioning.
- `Seed & Fixtures`: Seed data for development/testing.

**Tasks**:
- [ ] Define `Session`, `ArtifactSection`, `Trace`, `FeedbackLog`, `ApprovalLog`.
- [ ] Setup Alembic with `alembic.ini`, versions folder.
- [ ] Add helper to auto-generate migrations.
- [ ] Run initial migration.
- [ ] Write DB test to create and fetch model instance.

**Acceptance Criteria**:
- [ ] Models match schema from `reference_model.md`.
- [ ] Alembic can create DB from scratch.
- [ ] Model create/fetch/update tested.
- [ ] All required foreign key relations enforced.

**📂 Related System Design References**
- reference_model.md
- "Session, ArtifactSection, and Trace objects are persistable entities used across reasoning trace and planner."
- db_schema_notes.md
- "Describes relationships such as:"
    - "ArtifactSection -> many-to-one -> Session"
    - "Trace -> one-to-one -> ArtifactSection"
- system_architecture.md
- "DB stores persistent memory snapshots, tool call logs, and artifact content for versioning."
---

### WP3. Reference Loader

**Outcome**: Load gate reference YAML and make available to planner/tools.

**Scope**:
- `YAML Parsing`: Read `gate_reference.yaml`, normalize structure.
- `Caching`: Keep in-memory reference for reuse.
- `Access Layer`: Query by gate, artifact, or section.

**Tasks**:
- [ ] Create `services/reference_loader.py`.
- [ ] Write function to return artifacts by gate.
- [ ] Add loader tests for example YAML.
- [ ] Validate example/template ID resolution.

**Acceptance Criteria**:
- [ ] Can fetch full artifact spec by gate number.
- [ ] Unit tests cover 90%+ paths.
- [ ] Example/template links resolve to file path.
- [ ] Reference file can be hot-reloaded in dev mode.

**📂 Related System Design References**
gate_reference.yaml
→ Contains structured artifact definitions per gate:
gate: 1
artifacts:
  - name: Business Case
    sections:
      - section_id: rationale
        required_fields: [...]
        guidance: "State rationale..."
        example_id: bc_rationale_ex1
reference_model.md
→ "ReferenceLoader must parse gate_reference.yaml into in-memory ReferenceIndex and serve section templates, prompts, and validators."
tool_catalog.md
→ composeDraft, validateSection, and planner rely on section templates and guidance from the ReferenceIndex.

---

### WP4. Session Memory and YAML Workflow Engine

**Outcome**: Persistent and rehydratable session memory for document drafting.

**Scope**:
- `Session Storage`: Save YAML state to file/db.
- `Memory Modes`: Support “fresh”, “rehydrate”, “full doc” memory.
- `Trace Linking`: Link session to reasoning and planner logs.

**Tasks**:
- [ ] Create `session_memory.py`.
- [ ] Define memory schema.
- [ ] Implement read/write methods for each mode.
- [ ] Add `session_id` to all logs, commits.

**Acceptance Criteria**:
- [ ] Can initialize new session with metadata.
- [ ] Memory mode is switchable in planner.
- [ ] Section metadata is trace-linked.
- [ ] Session logs readable in UI.

**📂 Related System Design References**
session_memory_model.md
→ "Memory supports 3 modes: fresh, rehydrated (prior session), and full doc. Memory is backed by YAML files and supports merge + append operations."
reasoning_trace.yaml
→ YAML log includes session ID, memory snapshots, planner decisions, and tool chain steps.
reference_model.md
→ "SessionMemory is accessed via each tool, linked by section_id, document_id, or user_id. Memory state drives tool invocation planning."


---

### WP5. Google Drive Integration

**Outcome**: Full round-trip Drive integration with metadata.

**Scope**:
- `Drive Commit`: Upload docs with gate + section metadata.
- `Read Back`: Fetch and edit existing docs.
- `List View`: List documents by folder or tag.
- `Versioning`: Track edits with version history.

**Tasks**:
- [ ] Connect to Drive API with OAuth or service account.
- [ ] Write wrapper for upload, fetch, search.
- [ ] Write metadata tag schema.
- [ ] Create test doc from API call.

**Acceptance Criteria**:
- [ ] Docs can be uploaded and fetched with metadata.
- [ ] Upload includes gate, section, version fields.
- [ ] Returned doc content is accurate and latest.
- [ ] Sample section edit round-trip works.

---

### WP6. Planner and Outline Generator

**Outcome**: Convert user goals and gate into section-by-section task plan.

**Scope**:
- `Outline Planning`: Create `planner_task_trace.yaml`.
- `Tool Selection`: Assign tools (search, draft, validate).
- `Fallback Rules`: Handle missing input/evidence.

**Tasks**:
- [ ] Implement `generate_outline()` method.
- [ ] For each section, emit step plan with tools.
- [ ] Log planner trace for debugging.
- [ ] Unit test with sample goal and inputs.

**Acceptance Criteria**:
- [ ] Outline matches structure from reference.
- [ ] Task trace has correct tool sequence.
- [ ] Missing fields trigger “follow-up” or “search”.
- [ ] Trace is linkable to reasoning YAML.

---

### WP7. Reasoning Trace Capture

**Outcome**: Capture trace for each section from draft to commit.

**Scope**:
- `Trace Format`: Create `reasoning_trace.yaml` entries.
- `Validator Hits`: Log rule passes/fails.
- `Tool Chain Logging`: Log all tool calls per section.

**Tasks**:
- [ ] Define `ReasoningTrace` model + YAML schema.
- [ ] Hook trace logger into all tool endpoints.
- [ ] Test trace with 2+ section examples.

**Acceptance Criteria**:
- [ ] Trace shows tools used, prompts, evidence.
- [ ] Logs match planner plan.
- [ ] Validator outcomes are captured in trace.
- [ ] Test includes override path by user.

---

### WP8. Drafting Tools and Validator Layer

**Outcome**: Compose, validate, and finalize section drafts.

**Scope**:
- `Draft Generator`: GPT + template + memory + evidence.
- `Validator`: Structural and logical checks.
- `Fallback Loop`: Retry draft on fail.

**Tasks**:
- [ ] Implement `compose_and_cite()`.
- [ ] Build `validate_section()` rule engine.
- [ ] Write test with failing draft → regenerate.

**Acceptance Criteria**:
- [ ] Draft includes citations, fulfills schema.
- [ ] Fails trigger retry or feedback.
- [ ] Trace is updated on all passes/fails.
- [ ] Test run produces pass/fail report.

---

### WP9. Feedback Ingestion

**Outcome**: Apply reviewer feedback to section drafts.

**Scope**:
- `Comment Mapping`: PDF → section metadata.
- `Change Reasoning`: Highlight change rationale.
- `Version Tracking`: Link revision to Drive version.

**Tasks**:
- [ ] Parse annotated PDFs or YAML comments.
- [ ] Highlight affected fields in section.
- [ ] Append to `DocumentFeedbackLog`.

**Acceptance Criteria**:
- [ ] Review logs persist with timestamp.
- [ ] Updates merge cleanly with YAML.
- [ ] Test reviewer flow end-to-end.

---

### WP10. Input Ingestion & Summarizer

**Outcome**: Accept and process user-uploaded documents.

**Scope**:
- `File Upload`: Accept DOCX, PDF, TXT, YAML.
- `Summarization`: Extract key content into project memory.
- `Mapping`: Link findings to gate/section metadata.

**Tasks**:
- [ ] Build `upload_file()` endpoint.
- [ ] Write `summarize_input()` using GPT.
- [ ] Map content into `source_inputs.yaml`.

**Acceptance Criteria**:
- [ ] User can upload and summarize at least 3 file types.
- [ ] YAML generated is linked to draft planning.
- [ ] GPT summary is editable.
- [ ] Test flow produces usable inputs for planner.

---
