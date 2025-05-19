---

## title: API Contracts

## Overview

This document defines the API contracts used by the GPT agent and backend services to interact with the tools in PolicyGPT. Each contract includes endpoints, input/output schemas, validation logic, error handling rules, authentication, and versioning. The section ensures technical alignment with user journeys, features, and system constraints.

## Common API Patterns

### Authentication
- **Google Drive:** OAuth 2.0 service account or delegated user; token refresh handling.
- **Airtable:** API token in request header; validate token before execution.

### Input/Output Envelope
```json
{
  "status": "success" | "error",
  "data": {},
  "message": "Optional message",
  "timestamp": "ISO8601"
}
```

### Tool Invocation Lifecycle
1. GPT constructs tool call with expected input shape.
2. FastAPI validates request against OpenAPI schema.
3. Business logic executes (Drive, DB, search, etc.).
4. Response formatted using envelope schema.
5. Tool logs stored in PromptLog.

## Endpoint Contracts

### 1. `commitSection`
- **POST** `/commit_section`
- **Inputs:**
```json
{
  "project_id": "123",
  "section_type": "rationale",
  "content": "## Rationale\nThis project aligns with...",
  "language": "EN",
  "version": "v1.0",
  "reviewer_initials": "AB"
}
```
- **Outputs:**
```json
{
  "status": "success",
  "data": {
    "drive_url": "https://drive.google.com/file/d/xyz",
    "artifact_section_id": "sec123"
  },
  "timestamp": "2025-05-18T12:00:00Z"
}
```
- **Validation:**
  - `section_type` in allowed enum
  - `content` must be non-empty markdown
- **Error Responses:**
  - `400`: Missing required field
  - `403`: Permission denied (Drive)
  - `500`: Upload failure
- **Writes To:** Google Drive, ArtifactSection, FileMetadata

### 2. `commitDocument`
- **POST** `/commit_document`
- **Inputs:**
```json
{
  "project_id": "123",
  "section_ids": ["sec1", "sec2"],
  "title": "Gate 1 Submission",
  "language": "EN",
  "version": "v2.0",
  "gate_stage": "G1"
}
```
- **Outputs:**
```json
{
  "status": "success",
  "data": {
    "drive_url": "https://drive.google.com/file/d/abc",
    "document_id": "doc456"
  },
  "timestamp": "2025-05-18T12:01:00Z"
}
```
- **Validation:**
  - Validate `section_ids` are non-empty and exist
  - Total token count ≤ context limit
- **Error Responses:**
  - `400`: Token overflow
  - `404`: Section not found
- **Writes To:** Google Drive, ArtifactDocument, FileMetadata

### 3. `fetchDocument`
- **GET** `/fetch_document`
- **Inputs:**
```json
{
  "document_id": "doc456"
}
```
- **Outputs:**
```json
{
  "status": "success",
  "data": {
    "content": "## Gate 1 Submission\n...",
    "metadata": {}
  },
  "timestamp": "2025-05-18T12:02:00Z"
}
```
- **Error Responses:**
  - `404`: Document not found
  - `500`: Drive API error
- **Reads From:** Google Drive, ArtifactDocument

### 4. `searchKnowledgeBase`
- **POST** `/search_kb`
- **Inputs:**
```json
{
  "query": "governance models",
  "filters": {}
}
```
- **Outputs:**
```json
{
  "status": "success",
  "data": [
    { "title": "GC Governance Guide", "url": "https://..." }
  ],
  "timestamp": "2025-05-18T12:03:00Z"
}
```
- **Reads From:** ChromaDB

### 5. `externalWebSearch`
- **POST** `/web_search`
- **Inputs:**
```json
{
  "query": "federal digital policy outcomes"
}
```
- **Outputs:**
```json
{
  "status": "success",
  "data": [
    { "title": "OECD Digital Policy", "url": "https://..." }
  ],
  "timestamp": "2025-05-18T12:04:00Z"
}
```
- **Error Responses:**
  - `500`: External search failure

### 6. `queryAirtable`
- **POST** `/airtable_query`
- **Inputs:**
```json
{
  "table_name": "indicators",
  "query": "digital transformation"
}
```
- **Outputs:**
```json
{
  "status": "success",
  "data": [
    { "indicator": "access to broadband", "value": "85%" }
  ],
  "timestamp": "2025-05-18T12:05:00Z"
}
```
- **Error Responses:**
  - `403`: Invalid token
  - `404`: Table not found

### 7. `parseTranscript`
- **POST** `/parse_transcript`
- **Inputs:**
```json
{
  "transcript_text": "Stakeholder: We support the timeline..."
}
```
- **Outputs:**
```json
{
  "status": "success",
  "data": {
    "summary": "Stakeholders generally support the proposed timeline.",
    "topics": ["timeline", "support"]
  },
  "timestamp": "2025-05-18T12:06:00Z"
}
```

### 8. `loadCorpus`
- **POST** `/load_doc`
- **Inputs:**
```json
{
  "doc_url": "https://drive.google.com/...",
  "tags": ["privacy", "GC"]
}
```
- **Outputs:**
```json
{
  "status": "success",
  "data": { "doc_id": "kb789" },
  "timestamp": "2025-05-18T12:07:00Z"
}
```

### 9. `getTokenUsage`
- **GET** `/token_count`
- **Inputs:**
```json
{
  "prompt": "Generate a draft rationale section..."
}
```
- **Outputs:**
```json
{
  "status": "success",
  "data": {
    "token_count": 3456,
    "percent_used": 72
  },
  "timestamp": "2025-05-18T12:08:00Z"
}
```

### 10. `translateDocument`
- **POST** `/translate`
- **Inputs:**
```json
{
  "document_id": "doc456",
  "target_language": "FR"
}
```
- **Outputs:**
```json
{
  "status": "success",
  "data": {
    "translated_doc_url": "https://drive.google.com/file/..."
  },
  "timestamp": "2025-05-18T12:09:00Z"
}
```

## Unknowns, Risks, and Constraints

### Unknowns
- **Exact schema of Airtable datasets:** May change over time
- **Web search result variability:** Reliability of upstream sources

### Risks
- **Token overflow on large documents**
- **Drive or Airtable API downtime**
- **Invalid or malformed inputs from GPT**

### Mitigations
- **Schema validation layer** for Airtable + YAML
- **Retry + fallback cache** for Drive/Airtable
- **Preflight checks** for inputs, with safe defaults
- **Chunking** for large documents
- **Mock payload testing** before execution

## Tool Catalog Alignment

| Tool              | API Endpoint         | Contract Match | Notes                                                      |
|------------------|----------------------|----------------|------------------------------------------------------------|
| commitSection     | /commit_section      | ✅              | Handles markdown → Word/PDF; stores in DB + Drive         |
| commitDocument    | /commit_document     | ✅              | Stitching logic, Drive versioned upload                   |
| fetchDocument     | /fetch_document      | ✅              | Contextual fetch from DB or fallback from Drive            |
| searchKnowledgeBase | /search_kb         | ✅              | Indexed on upload; semantic rank on query                  |
| externalWebSearch | /web_search          | ✅              | Needed for credible research data                          |
| queryAirtable     | /airtable_query      | ✅              | Lookup for indicators, gate examples                       |
| parseTranscript   | /parse_transcript    | ✅              | Structured interview ingestion                             |
| loadCorpus        | /load_doc            | ✅              | Adds reference material to local KB                        |
| getTokenUsage     | /token_count         | ✅              | Context size tracking; informs chunking decisions          |
| translateDocument | /translate           | ✅              | Supports EN ⇆ FR; commits both versions                    |

## Error Response Recommendations

- **Standard JSON error format** with codes, message, trace_id
- Add tool-specific details, e.g. field name for 422 errors
- Log to PromptLog DB entry with retry flag
- Include recovery advice in response message

## External System Integration Patterns

### Google Drive
- Use service account token
- Refresh token before expiry
- Wrap upload in try/catch; fallback to local write
- Metadata includes gate, status, initials

### Airtable
- Personal access token in header
- Validate access by table name
- Queries mapped to internal lookup types (risks, benefits, precedents)

## Validation Mapping
- Preflight check (FastAPI schema validation)
- Tool-specific logic: quota check, type match, source safety
- DB constraint checks: section exists, unique filename

## Next Steps
- Add Swagger UI interface
- Export OpenAPI JSON for each endpoint
- Unit test harness for mock payloads
