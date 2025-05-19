## Error Handling Matrix (v2)

This document outlines how errors are detected, categorized, logged, and resolved across the PolicyGPT system stack, including GPT tools, FastAPI backend, database, external services, and user interactions. Enhancements include dynamic planner/tool integration, additional validation scaffolds, and retry visibility for reliability.

---

### 🔁 Error Handling Overview Table

| Layer          | Error Type                       | Detection Mechanism               | Handling Strategy                        | Logged In                    |
| -------------- | -------------------------------- | --------------------------------- | ---------------------------------------- | ---------------------------- |
| GPT Agent      | Invalid inputs / missing context | Prompt inspection + schema errors | Tool call retries + ask user for context | PromptLog, SessionLog        |
| FastAPI Tools  | Validation / schema mismatch     | Pydantic schema + OpenAPI rules   | 422 response + GPT fallback or log error | ToolLog, ErrorLog            |
| FastAPI Tools  | Tool chaining failure            | Code exception or null response   | GPT notified + fallback or skip          | ToolLog, ChainLog            |
| Planner Engine | No valid toolchain or task loop  | Internal reasoning trace step     | End planner run, log status              | TaskMetadata, ReasoningTrace |
| Google Drive   | API auth failure or rate limit   | HTTP response codes               | Retry with backoff, local save           | ExternalServiceLog           |
| Airtable       | Token failure or schema mismatch | Response body + validation errors | Use static YAML fallback                 | ExternalServiceLog           |
| ChromaDB       | No results or low match score    | Semantic match scoring            | Retry with broader query or use fallback | SearchLog, KBLog             |
| Web Search     | No credible results or timeout   | Status codes + content filters    | Skip + notify user                       | WebLog                       |
| Database       | Write fail / read missing entity | Exception handling                | Rollback transaction, retry              | DBLog, AuditTrail            |

---

### 🔂 Fallback and Recovery Patterns

* **Retry Queues**: Each failed tool call can be retried asynchronously with exponential backoff.
* **Planner Replan**: If reasoning trace breaks (e.g., missing required step), planner halts task and logs issue in `TaskMetadata`.
* **Fallback Prompts**: If tool chaining fails, GPT re-asks user or proceeds with best-effort output.
* **Local Caching**: For Drive/Airtable, fallback to cached or locally stored content.
* **YAML Snapshots**: All session state and project profiles cached in structured YAML for restore.
* **Chunked Upload**: If document exceeds token size or file size, it is chunked and retries issued per chunk.

---

### 🔧 Tool-Specific Error Scenarios

#### `commitSection`

* **Errors:** missing file path, invalid metadata, Drive write fail
* **Mitigations:** schema validation, Drive retries, YAML cache, planner task status update

#### `fetchDocument`

* **Errors:** file not found, auth failure
* **Mitigations:** file existence check, prompt user for alternate input, cache fallback

#### `searchKnowledgeBase`

* **Errors:** no match, query too broad/narrow
* **Mitigations:** retry with reformulated query, fallback to web search, planner abort if empty

#### `composeAndCite`

* **Errors:** failed citation validation, missing input data
* **Mitigations:** re-chain upstream tools (`searchKB`, `queryAirtable`), prompt user for confirmation

---

### 🧾 Logging and Alerting

| Log Type           | Captures                                           | Review Frequency |
| ------------------ | -------------------------------------------------- | ---------------- |
| PromptLog          | GPT inputs, tool calls, responses                  | Daily            |
| ToolLog            | Tool invocation start, end, success/fail           | Hourly           |
| ErrorLog           | 4xx/5xx FastAPI errors + exception stack traces    | Realtime         |
| ExternalServiceLog | Third-party errors with response body + timestamps | Realtime         |
| AuditTrail         | All document actions with user + tool trace        | Daily            |
| TaskMetadata       | Planner execution state + error chains             | Daily            |

---

### 📜 Validation Scaffolds

* **OpenAPI schema enforcement**: all GPT tool calls are preflight validated
* **getTokenUsage**: verifies section is within GPT token window before generating
* **Drive file check**: verifies upload and confirms metadata matches gate + version
* **YAML schema**: validates project profile and session files before reuse
* **Citation check**: ensures source link validity before drafting final output
* **Planner guardrails**: fail fast if required steps are skipped or no valid tool exists

---

### 🚨 Unknowns, Risks, Constraints

| Area         | Issue                                 | Mitigation                          |
| ------------ | ------------------------------------- | ----------------------------------- |
| Google Drive | Quota errors or file corruption       | Use version history + local copy    |
| Airtable     | API deprecation or token expiry       | Monitor token; fallback to YAML     |
| GPT Limits   | Tool response too long                | Chunk content + use token estimator |
| DB Sync      | Out-of-sync project state             | Lock YAML + DB on commit            |
| Planner      | Repeats tool loop or fails tool match | Planner trace abort + log           |

---

### 🗃️ Logging Storage Schemas (DB Tables)

```sql
CREATE TABLE ErrorLog (
    id SERIAL PRIMARY KEY,
    tool_name TEXT,
    error_message TEXT,
    status_code INTEGER,
    timestamp TIMESTAMP,
    context JSONB
);

CREATE TABLE ToolLog (
    id SERIAL PRIMARY KEY,
    tool_name TEXT,
    action TEXT,
    success BOOLEAN,
    timestamp TIMESTAMP,
    input_payload JSONB,
    output_payload JSONB
);

CREATE TABLE ExternalServiceLog (
    id SERIAL PRIMARY KEY,
    service_name TEXT,
    error_type TEXT,
    response_code INTEGER,
    response_body TEXT,
    timestamp TIMESTAMP
);

CREATE TABLE PromptLog (
    id SERIAL PRIMARY KEY,
    session_id TEXT,
    prompt_text TEXT,
    tool_called TEXT,
    response TEXT,
    timestamp TIMESTAMP
);

CREATE TABLE AuditTrail (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    document_id TEXT,
    action TEXT,
    timestamp TIMESTAMP,
    notes TEXT
);

CREATE TABLE TaskMetadata (
    task_id TEXT PRIMARY KEY,
    status TEXT,
    planner_notes TEXT,
    tools_attempted TEXT[],
    error_chain JSONB,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

---

### ✅ Next Actions

* [ ] Add planner-specific logging to `TaskMetadata`
* [ ] Implement retry queue tracking and metrics dashboard
* [ ] Add fallback result flag to PromptLog and DocumentVersion metadata
* [ ] Align all tool schemas to reflect error-resilience hooks (e.g., output status, fallback used)
* [ ] Create alerting logic for frequent failure patterns or GPT fallback overuse
