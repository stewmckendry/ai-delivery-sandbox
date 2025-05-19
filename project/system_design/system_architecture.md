---
title: System Architecture
---

## Overview

This document provides a high-level system architecture for PolicyGPT, aligned with the user journey, acceptance criteria, and technical components. It integrates both frontend GPT functionality and backend services, describing data flow, integration patterns, storage, and OpenAPI tooling.

## Architecture Layers and Components

### 1. UI/UX Layer
**Tech:** Custom GPT (OpenAI) + File Uploads

- **Function:** User-facing interface for writing, reviewing, and managing gate documents.
- **Inputs:** User prompts, file uploads (Word, PDF, Markdown, YAML).
- **Outputs:** Drafted gate artifacts (Markdown), responses, and file commits.
- **Process:** User interacts with PolicyGPT to generate or revise sections. GPT tools commit updates to backend services.
- **Enhancements:**
  - Enable UI prompts for switching between Canvas and External editing modes.
  - Add bilingual toggle and translation prompt interface.

### 2. Tool Backend (FastAPI)
**Tech:** Python + FastAPI + OpenAPI Tools

- **Function:** API layer handling document commit, fetch, export, and state synchronization.
- **Inputs:** Section metadata, content markdown, project and gate IDs, user IDs.
- **Outputs:** Stored documents in Google Drive, metadata logs.
- **Process:** Implements /commitSection and /commitDocument with support for versioning, metadata, and chunking.
- **Enhancements:**
  - Add /fetchDocument and /listFiles to pull Drive content and file listings.
  - Token counter to monitor session size and enable auto scale-out.
  - Implement validation, audit trail logging, and fallback upload support.

### 3. Knowledge Base
**Tech:** ChromaDB + sentence-transformers

- **Function:** Vector store for relevant project and policy content.
- **Inputs:** Reference documents, policy guidelines.
- **Outputs:** Retrieved semantic matches.
- **Process:** Embeds documents and queries for relevant sections.
- **Enhancements:**
  - Add YAML config for indexing metadata (e.g. gate stage, project ID).
  - Include auditor reports, prior GC submissions, policy directives.

### 4. Document Management
**Tech:** Google Drive API

- **Function:** Storage for draft/final project artifacts.
- **Inputs:** Markdown or Google Doc content, metadata.
- **Outputs:** Document URLs, revision history.
- **Process:** OAuth-authenticated access to Drive. Supports structured naming, version control, and folder hierarchies.
- **Enhancements:**
  - Enable round-trip editing via fetchDocument.
  - Metadata tagging (e.g. appProperties: gateStage, version).
  - Fetch folder listings and retrieve latest file versions.

### 5. Reference / Lookup Data
**Tech:** Airtable

- **Function:** Stores reference tables, indicators, mappings.
- **Inputs:** JSON schema, project-linked references.
- **Outputs:** Queried values.
- **Process:** Accessed via fetch_reference_table() and query_airtable().
- **Enhancements:** Display reference mappings in checklist tool.

### 6. Research Integration
**Tech:** Document corpus + optional web search

- **Function:** Supports precedent scans and comparative analysis.
- **Inputs:** Embedded documents or queries.
- **Outputs:** Matches to policy language, examples.
- **Process:** Uses ChromaDB and embedding search.
- **Enhancements:**
  - Index GC auditor reports, TBS policies, cross-jurisdiction examples.
  - Web search fallback for stats, studies, and external sources.
  - Use in Section Drafting for rationale, citations, and comparisons.

### 7. Meeting Capture
**Tech:** Otter.ai transcripts + parser tool

- **Function:** Converts transcripts to structured summaries.
- **Inputs:** .txt, .docx transcript files.
- **Outputs:** YAML summaries.
- **Process:** Parsed via FastAPI tool and summarized.

## System Design Documents

### system_architecture.md
This document itself.

### data_flow_master.md
Describes flow from prompt → GPT output → commit tool → Google Drive.

### db_schema_notes.md
Will define internal representations for documents, sections, projects, and revisions.

### tool_catalog.md
Catalog of OpenAPI endpoints: commitSection, commitDocument, fetchDocument, etc.

### api_contracts.md
Defines schemas and expected payloads for each tool. Includes required fields, validation logic, and versioning behavior.

### integration_points.md
Specifies connections across GPT ↔ FastAPI ↔ Google Drive ↔ Airtable ↔ ChromaDB.

### error_handling_matrix.md
Enumerates expected issues (e.g. token overuse, Drive errors) and resolution logic.

### session_memory_model.md
Outlines how memory is preserved across GPT sessions using project YAML and prompt engineering.

### reference_model.md
Describes domain concept: gate-based project lifecycle. Includes transitions (e.g. Gate 0 → Gate 1), states, artifacts.

## Implementation Patterns

- **Prompt Design:** Hierarchical, with system prompts for tone, length, and section headers.
- **Commit Patterns:** Incremental sections (via commitSection), final documents (via commitDocument).
- **File Storage:** Per-project folders in Drive; structured metadata for gateStage, version.
- **Sync Logic:** Fetch latest on user request; resolve version conflicts; chunk uploads if needed.
- **UX Modes:** Canvas-mode with GPT dialog, external-mode for Google Docs edits.
- **Token Tracking:** Uses token count to avoid overflow and apply chunking.
- **Audit Trails:** Metadata, timestamps, and rationale captured for legal defensibility.
- **Multilingual Support:** Store both EN and FR versions; translate via GPT tool.

## Feature and Acceptance Criteria Verification

Each layer/component of the architecture has been reviewed to confirm it supports the full PolicyGPT feature set and acceptance criteria:

| Component                 | Feature Alignment                                                                                 | Gaps Found            | Resolution                                                                 |
|--------------------------|--------------------------------------------------------------------------------------------------|------------------------|---------------------------------------------------------------------------|
| UI/UX Layer              | 2.1–2.8 tools, guided UX, toggle for bilingual, preview mode                                     | None                   | —                                                                         |
| Tool Backend             | Handles all OpenAPI tools, chunking, version control, audit logging                             | Needs listFiles tool   | Add endpoint for Drive folder listing                                    |
| Knowledge Base           | Supports 1.4 Evidence + Alignment Search                                                         | None                   | —                                                                         |
| Document Management      | Fully integrated with 1.2 + 2.7/2.8 needs; supports Drive commits, metadata, file versioning    | None                   | —                                                                         |
| Reference / Lookup Data  | Meets 1.1 schema, acceptance logic, maps, prompt examples                                        | None                   | —                                                                         |
| Research Integration     | Supports 1.4: evidence, alignment, GC reports, other jurisdictions                              | None                   | —                                                                         |
| Meeting Capture          | Aligned with 2.2 ingestion of transcripts                                                       | None                   | —                                                                         |
| YAML Profile Engine      | Shared across tools, inline editing supported, drives continuity                               | None                   | —                                                                         |
| Token Count Utility      | Monitors session size, applies chunking logic                                                   | None                   | —                                                                         |
| Export/Commit Tool       | Handles full file output, bilingual, metadata tagging, approvals                               | None                   | —                                                                         |

## Next Steps
- Finalize tool schemas in tool_catalog.md and api_contracts.md.
- Generate initial drafts for remaining system design docs.
- Configure backend with commit/fetch endpoints and OAuth integration.
- Begin implementation planning for Drive file listing and version fetch.

This architecture is consistent with the goals outlined in the PolicyGPT Implementation Specification, and now fully aligns with all current feature and acceptance criteria documents.