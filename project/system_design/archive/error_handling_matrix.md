---

## title: Error Handling Matrix

## Overview

This document outlines how errors are detected, categorized, logged, and resolved across the PolicyGPT system stack, including GPT tools, FastAPI backend, external services, and user interactions. It includes mitigation patterns, fallback strategies, and validation scaffolds to ensure system robustness.

## Error Handling Overview Table

| Layer            | Error Type                        | Detection Mechanism               | Handling Strategy                        | Logged In              |
|------------------|------------------------------------|------------------------------------|-------------------------------------------|-------------------------|
| GPT Agent        | Invalid inputs / missing context   | Prompt inspection + schema errors | Tool call retries + ask user for context | PromptLog, SessionLog  |
| FastAPI Tools    | Validation / schema mismatch       | Pydantic schema + OpenAPI rules   | 422 response + GPT fallback or log error | ToolLog, ErrorLog      |
| FastAPI Tools    | Tool chaining failure              | Code exception or null response   | GPT notified + fallback or skip          | ToolLog, ChainLog      |
| Google Drive     | API auth failure or rate limit     | HTTP response codes               | Retry with backoff, local save           | ExternalServiceLog     |
| Airtable         | Token failure or schema mismatch   | Response body + validation errors | Use static YAML fallback                 | ExternalServiceLog     |
| ChromaDB         | No results or low match score      | Semantic match scoring            | Retry with broader query or use fallback | SearchLog, KBLog       |
| Web Search       | No credible results or timeout     | Status codes + content filters    | Skip + notify user                       | WebLog                 |
| Database         | Write fail / read missing entity   | Exception handling                | Rollback transaction, retry              | DBLog, AuditTrail      |

---

## Fallback and Recovery Patterns

- **Retry Queues**: Each failed tool call can be retried asynchronously with exponential backoff.
- **Fallback Prompts**: If tool chaining fails, GPT re-asks user or proceeds with best-effort output.
- **Local Caching**: For Drive/Airtable, fallback to cached or locally stored content.
- **YAML Snapshots**: All session state and project profiles cached in structured YAML for restore.

---

## Tool-Specific Error Scenarios

### commitSection
- **Errors:** missing file path, invalid metadata, Drive write fail
- **Mitigations:** schema validation, Google Drive retries, YAML cache

### fetchDocument
- **Errors:** file not found, auth failure
- **Mitigations:** check file existence, prompt user for alternate input

### searchKnowledgeBase
- **Errors:** no match, query too broad/narrow
- **Mitigations:** retry with related query, fallback to web search

### queryAirtable
- **Errors:** auth fail, malformed response
- **Mitigations:** fallback to local YAML mirror

---

## Logging and Alerting

| Log Type         | Captures                                             | Review Frequency |
|------------------|------------------------------------------------------|------------------|
| PromptLog        | GPT inputs, tool calls, responses                    | Daily            |
| ToolLog          | Tool invocation start, end, success/fail             | Hourly           |
| ErrorLog         | 4xx/5xx FastAPI errors + exception stack traces      | Realtime         |
| ExternalServiceLog | Third-party errors with response body + timestamps | Realtime         |
| AuditTrail       | All document actions with user + tool trace          | Daily            |

---

## Validation Scaffolds

- **OpenAPI schema enforcement**: all GPT tool calls are preflight validated
- **getTokenUsage**: verifies section is within GPT token window before generating
- **Drive file check**: verifies upload and confirms metadata matches gate + version
- **YAML schema**: validates project profile and session files before reuse

---

## Unknowns, Risks, Constraints

| Area         | Issue                            | Mitigation                          |
|--------------|----------------------------------|-------------------------------------|
| Google Drive | Quota errors or file corruption | Use version history + local copy    |
| Airtable     | API deprecation or token expiry | Monitor token; fallback to YAML     |
| GPT Limits   | Tool response too long          | Chunk content + use token estimator |
| DB Sync      | Out-of-sync project state       | Lock YAML + DB on commit            |

---

## Alignment with Tool Catalog

Each tool explicitly declares:
- What errors are expected
- What validation is enforced
- What fallback path is available
- What logs are written

Example:
- **commitDocument** logs `ToolLog`, `ErrorLog`, and updates `AuditTrail`
- **translateDocument** uses Drive + external API, and falls back to original + flag for translation pending

---

## Logging Storage and Schemas

All logs are stored in PostgreSQL with the following tables and schemas:

### ErrorLog
```sql
CREATE TABLE ErrorLog (
    id SERIAL PRIMARY KEY,
    tool_name TEXT,
    error_message TEXT,
    status_code INTEGER,
    timestamp TIMESTAMP,
    context JSONB
);
```

### ToolLog
```sql
CREATE TABLE ToolLog (
    id SERIAL PRIMARY KEY,
    tool_name TEXT,
    action TEXT,
    success BOOLEAN,
    timestamp TIMESTAMP,
    input_payload JSONB,
    output_payload JSONB
);
```

### ExternalServiceLog
```sql
CREATE TABLE ExternalServiceLog (
    id SERIAL PRIMARY KEY,
    service_name TEXT,
    error_type TEXT,
    response_code INTEGER,
    response_body TEXT,
    timestamp TIMESTAMP
);
```

### PromptLog
```sql
CREATE TABLE PromptLog (
    id SERIAL PRIMARY KEY,
    session_id TEXT,
    prompt_text TEXT,
    tool_called TEXT,
    response TEXT,
    timestamp TIMESTAMP
);
```

### AuditTrail
```sql
CREATE TABLE AuditTrail (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    document_id TEXT,
    action TEXT,
    timestamp TIMESTAMP,
    notes TEXT
);
```

Each table includes time-based indexing for efficient retrieval and monitoring dashboards.
