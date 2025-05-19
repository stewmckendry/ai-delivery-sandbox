---

## title: Tool Catalog

## Overview

This document catalogs the tools available to the GPT agent and backend API for performing PolicyGPT tasks. Each tool includes function, inputs/outputs, implementation details, how it connects to user journeys and platform requirements, and dynamic invocation context.

## Tools

### 1. `commitSection`

- **Function:** Saves a single section of an artifact to Google Drive and database.
- **Inputs:**
  - `project_id`, `section_type`, `content`, `language`, `version`, `reviewer_initials`
- **Outputs:**
  - Google Drive URL of committed section
  - DB update to `ArtifactSection`
- **Process:**
  - Validate section completeness and formatting
  - Store markdown content in DB (ArtifactSection)
  - Convert to Word or PDF using Pandoc
  - Upload to Google Drive via API (update FileMetadata)
- **Failure Scenarios & Mitigations:**
  - Drive error → Retry with exponential backoff; fallback to local disk and alert user
  - API quota exceeded → Use service account pooling
- **Dynamic Invocation:** Triggered after user confirms section edit or after GPT generates a section using project YAML.
- **Mock Payload:**
  ```
  {
    "project_id": "123",
    "section_type": "rationale",
    "content": "## Rationale\nThe project aligns with...",
    "language": "EN",
    "version": "v1.1",
    "reviewer_initials": "AB"
  }
  ```
- **Examples:**
  - User finalizes "Project Rationale" → tool converts content, uploads, updates DB with URL and version.

### 2. `commitDocument`

- **Function:** Commits a composed full artifact document (multi-section) to Google Drive.
- **Inputs:**
  - `project_id`, `section_ids[]`, `title`, `language`, `version`, `gate_stage`
- **Outputs:**
  - Final document Drive link
- **Process:**
  - Fetch all `ArtifactSection` by ID
  - Validate content completeness and flow
  - Combine into full document using stitching logic
  - Upload to Google Drive, update `ArtifactDocument`, `FileMetadata`
- **Failure Scenarios & Mitigations:**
  - Missing sections → Alert user before commit
  - Token overflow → Use chunking logic before document assembly
- **Dynamic Invocation:** Triggered when user requests full document export.
- **Mock Payload:**
  ```
  {
    "project_id": "123",
    "section_ids": ["s1", "s2", "s3"],
    "title": "Gate 1 Charter",
    "language": "EN",
    "version": "v2.0",
    "gate_stage": "G1"
  }
  ```
- **Examples:**
  - User submits Gate 1 Charter; system builds full document with 5 sections, uploads and returns Drive URL

### 3. `fetchDocument`

- **Function:** Retrieves a full artifact or section from Google Drive or local DB
- **Inputs:** `document_id` or `section_id`
- **Outputs:** Content in markdown, word, or pdf
- **Process:** Uses cached DB content if possible, else fetch from Drive
- **Dynamic Invocation:** Used before edits or composition for context continuity

### 4. `searchKnowledgeBase`

- **Function:** Semantic search over reference documents
- **Inputs:** Query string, optional tags
- **Outputs:** Ranked results with doc ID, excerpt, source
- **Process:** Uses sentence-transformer and ChromaDB
- **Tool-Level Validation:** Verifies format, filters unsafe sources

### 5. `externalWebSearch`

- **Function:** Search the web for academic articles, government statistics, international policy examples
- **Inputs:** Query string, filters (optional)
- **Outputs:** Ranked links with metadata and snippets
- **Process:** Uses SerpAPI or Bing API, caches results, verifies source credibility
- **Tool-Level Validation:** Flags non-credible domains, alerts user

### 6. `queryAirtable`

- **Function:** Lookup structured GC metadata (risk indicators, gate precedents, benefit types)
- **Inputs:** Table name, filters
- **Outputs:** JSON records
- **Data Source:** Curated and periodically refreshed from ResultsInfo, GC datasets, manually loaded references
- **Process:** Used to auto-populate checklists or suggest precedent text blocks
- **Example:** Get risk indicators for digital projects, previous Gate 2 cost ranges

### 7. `parseTranscript`

- **Function:** Extract structured YAML from meeting transcript
- **Inputs:** Transcript file (docx/txt)
- **Outputs:** YAML summary

### 8. `loadCorpus`

- **Function:** Add new documents to knowledge base
- **Inputs:** Doc file
- **Outputs:** Success status, vector index update

### 9. `getTokenUsage`

- **Function:** Monitors session token count for GPT context management
- **Inputs:** Session ID or prompt text
- **Outputs:** Token count and % used

### 10. `translateDocument`

- **Function:** Converts EN ⇆ FR using translation service
- **Inputs:** Section or document markdown
- **Outputs:** Translated version

## Enhancements Summary

- **Dynamic Invocation:** Clearly documented for key tools
- **Tool-Level Validation:** Field format, completeness, and source safety
- **Mock Payloads:** Provided for major tools

## Additional Recommendations Implemented

- Clarified when tools are invoked by GPT context (user requests, missing data, system thresholds)
- Added mock input/output for key tools to aid implementation
- Expanded on validation logic per tool to improve robustness
- Annotated DB schema and Drive update impact inline for traceability

## Detailed Examples by User Journey

### Journey A: Structured Iteration

1. User uploads notes → `parseTranscript`, `loadCorpus`
2. User requests Gate 0 artifact → `queryAirtable`, `searchKnowledgeBase`, `externalWebSearch`, `fetchDocument`
3. GPT suggests outline → `getTokenUsage`
4. User provides more info → `commitSection`, `getTokenUsage`
5. Each section is iterated and stored → `commitSection`
6. Final document composed → `commitDocument`
7. Optional translation → `translateDocument`

### Journey B: Check-the-Box

1. User uploads required inputs → `loadCorpus`, `parseTranscript`
2. Requests full draft → `searchKnowledgeBase`, `externalWebSearch`, `queryAirtable`, `getTokenUsage`
3. System chunks + generates each section → `commitSection`
4. Final doc created and stored → `commitDocument`, `translateDocument`

### Journey C: Review and Revise

1. Reviewer comments uploaded → `parseTranscript`, `loadCorpus`
2. GPT integrates changes → `fetchDocument`, `commitSection`
3. Re-review loop → `getTokenUsage`, `commitDocument`

## Alignment with DB Schema Notes

- **ArtifactSection** ↔ `commitSection`, `fetchDocument`
- **ArtifactDocument** ↔ `commitDocument`, `translateDocument`
- **PromptLog** ↔ internal logging during all GPT tools
- **FileMetadata** ↔ `parseTranscript`, `loadCorpus`
- Ensures each tool directly updates and reads DB tables as needed

## Verification Against Features, Journeys, and A/C

### Coverage Map

#### Feature Support

- Audit trails: `commitSection`, `PromptLog` DB
- Metadata tagging: All commit tools
- Structured edits: `parseTranscript`, `searchKnowledgeBase`
- Bilingual outputs: `translateDocument`
- Evidence support: `searchKnowledgeBase`, `externalWebSearch`, `queryAirtable`, `loadCorpus`
- Approvals history: `commitDocument`, `ArtifactDocument`
- Input quality: `parseTranscript`, `searchKnowledgeBase`, `externalWebSearch`
- Formal drafting: `commitSection` with YAML profile references
- Project state tracking: `getTokenUsage`, `fetchDocument`

### Gaps Found and Fixed

- Missing metadata handling clarified
- Translation and token usage explicitly documented
- Integrated YAML and DB schema alignment
- Added external evidence search coverage via `externalWebSearch`

## Alignment with Features and Acceptance Criteria

### Coverage Validation

- **Document storage and versioning:** Covered by `commitSection` and `commitDocument` with versioning logic.
- **Evidence and research sourcing:** Covered by `searchKnowledgeBase`, `externalWebSearch`, `queryAirtable`, `loadCorpus`. Returns stats, policies, academic papers, prior GC initiatives.
- **Input reuse and progressive drafting:** Drafting history and edits handled through `fetchDocument`, with updates via `commitSection`. Token tracking with `getTokenUsage` helps chunking.
- **Formal government artifact quality:** Outputs from `commitSection` expected to match tone, formatting and thoroughness required for federal gates.
- **Bilingual output generation:** `translateDocument` directly supports FR generation; outputs stored in DB and Drive.
- **Audit, approvals, and logging:** `PromptLog`, `ArtifactDocument`, and `commitDocument` ensure legal traceability.
- **Fallback logic for uploads:** If `loadCorpus` or `parseTranscript` fail, users are notified and prompted to upload manually.
- **Guided inputs and checklists:** `parseTranscript`, `queryAirtable`, `searchKnowledgeBase`, `externalWebSearch` prompt for missing info, feed validations.
- **Section-to-document flow assurance:** Token checks and stitching logic ensure continuity between sections → document → review.

### Enhancements Made

- Added `getTokenUsage` to support scaling out sessions
- Included upload fallback for parsing tools
- Clarified full-document handling for translations and formal quality
- Defined examples for multi-tool flows per user journey
- Introduced `externalWebSearch` to support external evidence

## Technology Constraints and Mitigations

- **Token limits:** Use `getTokenUsage`, chunking, and stitching logic
- **Drive latency:** Retry logic, fallback disk cache
- **Rate limits:** API quotas managed via pooled service accounts
- **Search index staleness:** Scheduled retraining + `loadCorpus` hooks
- **External API reliability:** Add redundancy between `searchKnowledgeBase` and `externalWebSearch` with fallbacks

## Unknowns and Risks

- **File structure assumptions:** Mitigate with schema detection
- **Translation quality:** Fallback to user-reviewed plain text
- **Session memory loss:** Ensure YAML regeneration each session

## Next Steps

- Add unit tests for each tool
- Create mock payload examples
- Add ER diagrams and flow charts for tool interactions
