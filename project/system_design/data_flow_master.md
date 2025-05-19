---
title: Data Flow Master
---

## Overview
This document describes how data flows through the PolicyGPT system from initial user inputs to final artifact export. It aligns with the user journey, system architecture, and feature requirements.

## High-Level Flow

1. **User Initiation**  
   - Input: User prompt or request (e.g., "Start Gate 0 draft")  
   - Tools: PolicyGPT (GPT front-end)

2. **Requirement Lookup**  
   - Tool: Reference Lookup Tool  
   - Action: Fetch gate artifact templates and checklists from Airtable or gate_reference.yaml

3. **Input Ingestion**  
   - Tool: IngestInput tool  
   - Input: Uploaded files (.docx, .txt, .md, .pdf, .yaml)  
   - Output: Parsed YAML project profile + embedded reference data  
   - Mitigation: Validate inputs, show tips for good inputs, fallback to interview-style questions

4. **Evidence & Alignment Search**  
   - Tools: EvidenceSearch (web and document corpus) + AlignmentSearch (GC guidance, past projects, AG reports, policy scans)  
   - Output: Semantic matches, citations, statistics, reports, examples from other jurisdictions, and market scan results  
   - Mitigation: Clearly separate external vs internal search logic, include fallback examples from stored precedents

5. **Outline + Section Drafting**  
   - Tool: SectionDrafting tool  
   - Input: YAML profile, user instructions, precedents, templates, evidence  
   - Output: Markdown draft sections with embedded metadata  
   - Mitigation: Apply formal tone, completeness checklists, prompt for citations and evidence-based content, validate GPT token limits, use chunking as needed

6. **Iterative Review**  
   - Tool: Canvas Editor + commitSection tool  
   - Action: Draft refined section-by-section. Metadata applied: gateStage, sectionType, draftStatus, lastEditor, etc.  
   - Mitigation: Retrieve latest draft version from Drive before edit; auto-track session continuity with YAML

7. **Validation**  
   - Tool: Validator/Checklist AI  
   - Input: Draft YAML + rules  
   - Output: Flags for missing rationale, scope, metrics, alignment  
   - Mitigation: Update validators using gate_reference.yaml rules; allow user override with justification

8. **Document Composition and Editing**
   - Tool: DocumentComposer tool + CanvasEditor  
   - Action:  
     - Compose the full document by sequentially fetching sections from Drive.  
     - Assemble using YAML outline continuity to maintain logical order and flow.  
     - Present full document in Canvas for final review and editing.  
     - On edit, detect modified sections and update them individually via commitSection or regenerate outline where needed.
   - Mitigations for Token/API Limits:
     - **Fetch in Chunks**: Pull only 1–3 sections at a time using fetchDocument(section=...).
     - **Streaming Assembly**: Compose document incrementally and monitor cumulative token count.
     - **Memory Anchors**: Use persistent project YAML + outline as memory base to ensure continuity.
     - **Edit Buffering**: User edits in Canvas are saved section-by-section before reassembly.
     - **Staged Submission**: After review, commitDocument chunks content as needed for Drive storage (e.g., separate doc per 10-page limit).
     - **Background Retry Queue**: Use retry logic if export fails mid-upload due to file size.

9. **Finalization + Commit**  
   - Tool: commitDocument tool  
   - Output: PDF, Google Doc, Word; bilingual support; Drive URLs with metadata, version tags  
   - Mitigation: Chunk content if needed to avoid truncation; ensure both EN and FR versions committed

10. **Fetch + Revise**  
    - Tool: fetchDocument tool  
    - Action: Retrieve latest from Drive, re-commit revisions, track approvals  
    - Mitigation: Use Drive folder listings to find the latest; preserve version history with reviewerInitials

## Transformation Points

- Transcripts → YAML summaries (meeting capture parser)
- Documents → Embedded vectors (ChromaDB)
- Prompts → Structured responses (prompt chaining)
- YAML + Markdown → Word/PDF (Pandoc, WeasyPrint)

## Data Objects and Metadata

- **Project Profile YAML**: Core context object (title, rationale, outcomes, stakeholders)
- **Artifact Sections**: Markdown with metadata
  - Keys: sectionType, gateStage, draftVersion, reviewerInitials
- **Audit Log**: Timestamp, userID, prompt summary, version

## Verification Against Features and Acceptance Criteria

### 1.1 YAML Profile Engine
- ✅ Profile is generated early (step 3) and reused throughout.
- ✅ Guides section drafting, checklist validation, and document assembly.

### 1.2 File Integration
- ✅ Inputs parsed from multiple formats.
- ✅ fetchDocument and listFiles cover Drive retrieval + latest file access.
- ✅ commit tools handle file creation and updates.

### 1.3 Metadata Persistence
- ✅ commitSection and commitDocument embed sectionType, gateStage, draftStatus, reviewerInitials.
- ✅ Metadata travels with each draft and is stored in Drive.

### 1.4 Evidence and Alignment
- ✅ Separate tools for web search, document corpus, GC references.
- ✅ Precedent examples, stats, AG reports captured.

### 1.5 Token Limits
- ✅ Token count tracked at every step to determine need for chunking.
- ✅ Full chat token usage monitored to determine when to scale out.

### 2.2 Input Ingestion
- ✅ Supports upstream artifacts, transcripts, reference tables.
- ✅ Aligns with section templates.

### 2.3–2.6 Section Generation
- ✅ Drafted in markdown in Canvas.
- ✅ Formal tone, detailed structure.
- ✅ Fetches latest to update.
- ✅ Produces content at quality expected for large federal projects.

### 2.7 Document Export
- ✅ Full documents committed via commitDocument.
- ✅ Output formats include PDF, Word, Google Doc.
- ✅ Supports chunked large content.

### 2.8 Bilingual Support
- ✅ Final versions saved in EN and FR.
- ✅ Translation handled via prompt toggle or translation tool.

## Risks, Assumptions & Mitigations

| Assumption | Risk | Mitigation |
|------------|------|------------|
| Users upload quality files | Unstructured inputs hinder processing | Input guidance and fallback prompts |
| Drive structure is stable | Folder errors disrupt file flow | Auto-check and create paths |
| Outline sequence followed | Section misalignment | Enforce outline checkpoints |
| Validator rules are complete | Missed gate criteria | Regular rule updates and override logic |
| Session data retained | Fragmented drafts | Auto-fetch latest YAML at start |
| FR translation is formal | Quality/compliance risks | Dual-column preview + optional service integration |

## Technology Constraints and Mitigations

| Constraint | Impact on Data Flow | Mitigation |
|-----------|---------------------|------------|
| **Token Limits (OpenAI API)** | Full documents can't be processed at once | Use chunking and YAML outlines to handle one section at a time |
| **File Size Limits (Google Drive API, PDF/Word export)** | Large outputs may truncate or error during export | Use streaming write, paginate sections, and chunk commits |
| **Asynchronous Tools** | Delay between input and output across tools | Include job status polling and retry logic |
| **Rate Limits (Drive, Airtable APIs)** | Integration calls may be throttled | Batch requests, cache responses, and prioritize prefetching |
| **YAML Complexity / Schema Drift** | Profile files can break parsing | Validate schema on load, fall back to defaults, schema version tags |
| **Drive Folder Permissions** | Users may lack write access to paths | Auto-check/create folders; fallback to local save with alert |
| **Google Drive Auth** | OAuth flow complexity in GPT tool | Use service account with delegated domain-wide access |
| **Translation Inconsistency** | FR versions may lose fidelity | Use EN as source of truth, store both versions, and allow manual revision |
| **Session Volatility (GPT Memory)** | Loss of context across calls | Anchor with YAML, use reference prompts, auto-load project context each time |
| **Inter-tool Format Drift** | Markdown/YAML/pdf output inconsistencies | Use standard converters (Pandoc, WeasyPrint), test format round-trips |

## Next Steps
- Visualize data flow as diagram.
- Annotate transformation and sync points.
- Ensure validators cover all required metadata keys and audit fields.
