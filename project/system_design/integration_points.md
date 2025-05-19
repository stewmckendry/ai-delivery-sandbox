---

## Integration Points

## Overview

This document outlines how various system components—GPT, FastAPI tools, database, and external services—interconnect within PolicyGPT. It provides integration patterns, scaffolds for each connection, and how orchestration, fallback, and context continuity are handled.

## Integration Overview Table

| Component     | Connects To         | Method             | Fallbacks / Resilience       |
| ------------- | ------------------- | ------------------ | ---------------------------- |
| GPT Agent     | FastAPI Tools       | OpenAPI tool calls | Retry with default payloads  |
| FastAPI Tools | PostgreSQL DB       | SQLAlchemy ORM     | Local cache + error log      |
| FastAPI Tools | Google Drive API    | REST API + OAuth   | Local save + retry           |
| FastAPI Tools | Airtable API        | REST API + API key | Cached reference files       |
| FastAPI Tools | ChromaDB (KB)       | Python SDK         | Fallback to file search      |
| FastAPI Tools | External Web Search | REST call          | Notify user + skip fallback  |
---

## Interface Contracts

- All APIs follow a common envelope: `status`, `data`, `message`, `timestamp`
- Validations handled in FastAPI (input types, token limits, content safety)
- GPT builds payloads using structured prompt instructions

## Integration Details by System

### GPT ↔ FastAPI Tools

- **Pattern**: Tool invocation with schema validation.
- **Mechanism**: GPT uses OpenAPI schema to invoke backend endpoints with parameters.
- **Orchestration**: Conditional logic in GPT’s prompt engineering decides whether to invoke a tool based on missing info, input quality, or workflow step.
- **Chaining Logic**: Responses from one tool are used to invoke another. Prompt tracks state using YAML and tool output structure.
- **Fallbacks:** Validation errors, malformed JSON trigger fallback messages and retries.
- **Security:** GPT only calls whitelisted tool endpoints.

#### Tool Chaining Example

```python
# GPT Response Handling for Tool Chaining
if not user_inputs.get('rationale'):
    call_tool('search_kb', {query: 'project rationale examples'})
    call_tool('commitSection', {...})
```

---

### FastAPI ↔ PostgreSQL

- **Pattern**: SQLAlchemy ORM mapped to models.
- **Stored Entities**: `ProjectProfile`, `ArtifactSection`, `ArtifactDocument`, `PromptLog`, `FileMetadata`
- **Read:** `searchKnowledgeBase`
- **Write:** `loadCorpus`
- **Index:** Embeds uploaded docs using sentence-transformers.
- **Query:** Semantic match by cosine distance.
- **Fallback:** Use GPT web search if KB has no result.

* **Write Scaffold:**

```python
# Save ProjectProfile
profile = ProjectProfile(id=project_id, goals='...', scope='...')
db.session.add(profile)
db.session.commit()
```

- **Read Scaffold:**

```python
# Fetch Project Section
section = db.query(ArtifactSection).filter_by(project_id=pid, section_type='rationale').first()
```

- **Project Profile Includes:**
  - `project_id`, `goals`, `scope`, `risks`, `stakeholders`, `gate_status`, `approvals`, `language`
  - Stored in PostgreSQL and updated throughout GPT session lifecycle.

---

### FastAPI ↔ Google Drive

- **Pattern**: REST API v3 + OAuth 2.0
- **Purpose**: Commit documents, fetch versions, list files
- **Read:** `fetchDocument`, `loadCorpus`
- **Write:** `commitSection`, `commitDocument`, `translateDocument`
- **Mechanism:** OAuth 2.0 token; Drive API v3.
- **Metadata Layer:** Drive file metadata includes gate, version, reviewer, and status.
- **Retry Logic:** Auto-retry on 500 errors or token expiry

* **Scaffold:**

```python
# Upload
creds = get_google_creds()
service = build('drive', 'v3', credentials=creds)
file_metadata = {'name': 'Gate0_Summary.md'}
media = MediaFileUpload('doc.md', mimetype='text/markdown')
service.files().create(body=file_metadata, media_body=media).execute()

# Fetch
file_id = 'abc123'
file = service.files().get_media(fileId=file_id).execute()
```

---

### FastAPI ↔ Airtable

- **Pattern**: HTTP POST with API key
- **Used For**: Reference tables (e.g., GC indicators, benefits, precedent mappings)
- **Read Only:** `queryAirtable`
- **Tables Queried:** indicators, risk/benefit examples, success factors, precedent links.
- **Mechanism:** Personal access token; REST API with filterByFormula.
- **Schema Mapping:** Mapped to internal YAML scaffolds and section templates.
- **Error Handling:** Table/schema validation; fallback = static YAML dump.

* **Scaffold:**

```python
headers = {'Authorization': 'Bearer ' + AIRTABLE_TOKEN}
url = f'https://api.airtable.com/v0/{base_id}/{table_name}'
resp = requests.get(url, headers=headers)
data = resp.json()
```

---

### FastAPI ↔ ChromaDB

- **Pattern**: Embedding + vector search
- **Used For**: Semantic retrieval of stored documents
- **Scaffold:**

```python
kb = Chroma(collection='policy_corpus')
kb.add_document(doc_id='abc', content='...')
kb.query('project rationale')
```

---

### FastAPI ↔ External Web Search

- **Pattern**: API call to search index (e.g., SerpAPI, Bing)
- **Purpose**: Sourcing credible statistics, external reports, case studies
- **Scaffold:**

```python
query = 'government digitization outcomes'
results = search_web(query)
return results[:3]
```

---

## Verification with Features and Acceptance Criteria

Each integration directly maps to features and A/Cs:

- **Google Drive**: Used for commitSection, commitDocument, version control, bilingual storage → aligns with 2.7, 2.8
- **Airtable**: Lookup tables (risks, indicators, examples) → supports 1.4, 2.3
- **ChromaDB**: Stores and queries structured knowledge (GC docs, strategies) → supports research-based justification, 2.3
- **External Search**: Pulls evidence, precedent examples → supports 1.4, 2.3
- **DB**: Stores all content metadata, logs, project profiles → aligns with 1.5, 2.2, 2.3, 2.6

---

## Unknowns, Risks, Constraints

| Area         | Issue                               | Mitigation                               |
| ------------ | ----------------------------------- | ---------------------------------------- |
| Airtable     | Schema mismatch or rate limit       | Validate schema; add local fallback      |
| Drive        | Upload failure, API downtime        | Retry logic; allow local save            |
| Chroma       | Inaccurate ranking, stale data      | Periodic re-index; fallback to Drive     |
| GPT Tool Use | Tool invocation error (bad payload) | Mock tests + preflight schema validation |
| State Sync   | Project profile inconsistency       | YAML lockfile + DB sync                  |

---

## External System Patterns

### Google Drive

- Token refresh scheduled every 30 minutes
- Metadata normalization at upload (gate, initials, version)
- Folder creation by project ID

### Airtable

- Schema drift monitored via test queries
- Fallback to local YAML lookup if token fails or API quota exceeded

### ChromaDB

- Index rebuilt nightly
- New uploads embedded in batch job (or on-demand by `loadCorpus`)

### Web Search

- Caches last 10 queries
- Filters unsafe or low-trust domains using regex allowlist

## Validation Mapping

- Tools run preflight input validation via FastAPI schema
- Token usage estimated with `getTokenUsage` before section commit
- Section and document DB checks: existence, linkage, draft state

## Unknowns, Risks, and Constraints

- **Risk:** Airtable schema changes or API rate limits → mitigation: local YAML mirror
- **Unknown:** ChromaDB scale under large KB sizes → monitor vector cache size
- **Constraint:** Token limits for GPT calls → mitigate via `getTokenUsage` + chunking



## Next Steps

- Add retry queue per tool with alerts
- Map external service dependencies with latency thresholds
- Add Swagger test scaffolds to each integration call

##