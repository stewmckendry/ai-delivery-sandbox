# PolicyGPT Feature Breakdown

This document outlines the functional and technical components required to implement PolicyGPT. Features are organized into foundational work packages and user-facing tools, and mapped to user journeys.

---

## 1. Foundational Work Packages

### 1.1 Document and Metadata Reference Layer
- **Description**: Source of truth for gating criteria, artifact templates, document types, required inputs, acceptance criteria, and prompt examples. It includes artifact-specific structures (e.g., financial tables, HR plans), terminology, and compliance formats tailored to GC standards.
- **Examples**: YAML file for Gate 0 containing list of artifacts (e.g., Investment Proposal, Risk Register), required fields, example prompts, default templates for risk analysis.
- **In Scope**: YAML + markdown templates, example prompts, validation logic, evidence requirements, alignment mappings.
- **Out of Scope**: Live syncing with external policy databases.
- **Tasks**:
  - Build and version reference YAML files.
  - Define schema and example prompts.
  - Map prompts and artifacts to departmental policies and GC priorities.
  - Load into ChromaDB.
- **Design Decisions**:
  - Treat prompt examples as metadata fields.
  - Each artifact has its own reference entry.
  - Maintain linkage to source policy directives.
- **Acceptance Criteria**:
  - Reference files can be queried by gate, artifact, or input need.
  - Includes example schema-aligned drafting prompts and acceptance checklists.
  - Maps include artifact-specific formatting and terminology requirements.

### 1.2 Google Drive Integration
- **Description**: Tools to commit, fetch, and search versioned documents.
- **Examples**: Committing a section with `commitSection`, returning URL with metadata.
- **Tasks**:
  - Implement Drive upload API.
  - Store metadata alongside each file.
  - Provide secure fetch and search.
  - Search previous artifacts and precedents to support drafting.
- **Acceptance Criteria**:
  - Commit returns shareable Drive URL with version tag.
  - Fetch tool supports version filtering and metadata search.
  - Files and metadata are used in subsequent section drafting.

### 1.3 YAML Project Profile Engine
- **Description**: Holds core project inputs (goal, scope, stakeholders, risks) that inform drafting.
- **Tasks**:
  - Define project profile schema.
  - Populate with user inputs or GPT-synthesized info.
  - Sync across all sections.
- **Design Decisions**:
  - Used by section drafting tools to maintain continuity.
- **Acceptance Criteria**:
  - All artifact sections use consistent inputs and tone from profile.
  - Profile is editable and shared across tools.

### 1.4 Evidence and Alignment Search
- **Description**: Comprises two parts:
  - **External Evidence Search**: StatsCan, academic databases, OECD, GC portals.
  - **Internal Alignment Search**: Previously ingested GC guidance, mandates, strategic plans.
- **Function**: Supports rationale development, citations, alignment with strategy.
- **Inputs**: Section topic, context, metadata tags.
- **Outputs**: Structured snippets, citations, source links.
- **Process**:
  - Run web search or query local indexed sources.
  - Match results to section needs (e.g., problem statement).
  - Format for inclusion in content.
- **Tasks**:
  - Integrate external plugins.
  - Build internal ChromaDB index.
  - Enable section-level evidence search.
- **Acceptance Criteria**:
  - Supports structured evidence prompts.
  - Results used in justification blocks.
  - Can be traced to original source.

### 1.5 Token Count Utility
- **Function**: Checks token count and flags limits.
- **Inputs**: Draft section, outline, profile.
- **Outputs**: Token alert or chunking plan.
- **Process**:
  - Count input/output tokens per section.
  - Split content or compress if needed.
- **Tasks**:
  - Build count + warning logic.
  - Auto-chunk if needed.
- **Acceptance Criteria**:
  - Avoids token overflow errors.

---

## 2. Core User Tools

### 2.1 Artifact Lookup & Checklist Builder
- **Function**: Retrieves artifact list and requirements per gate.
- **Inputs**: Gate number
- **Outputs**: Checklist with required docs, guidance
- **Process**:
  - Query 1.1 Reference Layer by gate
  - Present checklist and links
- **Enhancements**:
  - Shows good examples, tips
  - Highlights acceptance criteria

### 2.2 Input Ingestion & Summarizer
- **Function**: Upload, read, and synthesize user-provided materials.
- **Inputs**: Transcripts, notes, PDFs
- **Outputs**: YAML summary for 2.3
- **Process**:
  - OCR or parse uploads
  - Identify themes, entities, insights
  - Generate structured YAML
- **Enhancements**:
  - Precedent search from similar docs
  - Filetype fallback logic

### 2.3 Section Drafting Tool
- **Function**: Prompts for inputs and generates each artifact section
- **Inputs**: YAML summary, project profile, evidence search results
- **Outputs**: Draft section
- **Process**:
  - Load section structure from 1.1
  - Ask guided questions per schema
  - Pull supporting data from profile and 1.4
  - Validate against required fields
- **Enhancements**:
  - Alignment validation to GC goals
  - French/English drafting
  - Insert precedents

### 2.4 Section Iteration Engine
- **Function**: Iterates on section drafts with user
- **Inputs**: Section draft, user feedback
- **Outputs**: Updated draft, audit trail
- **Process**:
  - Edit in GPT canvas
  - Capture rationale
  - Validate and commit to Drive
- **Enhancements**:
  - Chain-of-thought storage
  - Context continuity via project profile

### 2.5 Full Document Composer
- **Function**: Assembles complete document
- **Inputs**: All committed sections, outline
- **Outputs**: Composed draft
- **Process**:
  - Retrieve sections
  - Use outline and project profile for flow
  - Stitch with transitions
- **Enhancements**:
  - Preview mode
  - Style validation

### 2.6 Feedback Ingestion Tool
- **Function**: Reads and integrates reviewer feedback
- **Inputs**: Comments, annotated files
- **Outputs**: Redlines, updated content
- **Process**:
  - Summarize feedback
  - Suggest edits
  - Integrate and revalidate
- **Enhancements**:
  - Track comment source
  - Link edits to approval history

### 2.7 Export and Commit Tool
- **Function**: Finalizes and saves to Drive
- **Inputs**: Final document, metadata
- **Outputs**: URL, status tags, logs
- **Process**:
  - Generate PDF/Word
  - Apply version label
  - Store and log metadata
- **Enhancements**:
  - Support approvals, redactions
  - Time-stamped chain-of-thought

### 2.8 Translation and Bilingual Tool
- **Function**: Translate document
- **Inputs**: English or French content
- **Outputs**: Other language draft
- **Process**:
  - Translate using prompt tuning or plugin
  - Validate format
- **Enhancements**:
  - Auto or manual mode

### 2.9 Version and Approval History Tracker
- **Function**: Track approvals and versions
- **Inputs**: Commit metadata
- **Outputs**: Checklist with reviewer names, versions
- **Process**:
  - Log each commit
  - Associate reviewers
- **Enhancements**:
  - Store signed versions
  - View history with filters

---

## 3. User Journey Overlay

### Journey A: Structured Iteration (Primary Path)
1. **User** says they need to prepare artifacts for Gate 0.
   - **Tool**: 2.1 Artifact Lookup retrieves required docs.
2. **PolicyGPT** looks up requirements from reference layer.
   - **Tool**: 1.1 Document and Metadata Reference Layer.
3. **PolicyGPT** presents a checklist, requests inputs, and provides guidance.
   - **Tool**: 2.1 Checklist Builder + examples from 1.1.
4. **User** uploads transcripts, notes, and prior docs.
   - **Tool**: 2.2 Input Ingestion (with fallback logic).
5. **PolicyGPT** reads files, synthesizes inputs, maps to artifacts.
   - **Tool**: 2.2 Input Ingestion & 2.3 Section Drafting.
   - Prompts again for missing rationale, citations, or data.
   - Leverages 1.3 YAML Profile to inform section drafts.
   - Uses 1.4 to search for evidence or alignment.
6. **GPT** iterates with user in canvas per section.
   - **Tool**: 2.4 Section Iteration (with audit annotations).
   - Drafts are stored to Drive and traced with metadata.
7. **User** previews assembled doc before commit.
   - **Tool**: 2.5 Full Composer uses outline continuity.
8. **GPT** commits final to Google Drive with metadata.
   - **Tool**: 2.7 Export Tool.
   - Metadata includes draft status, version, gate, reviewer.
   - Version history tracked via 2.9.

### Journey B: Check-the-Box Generation
1. **User** uploads all required materials and says "Just generate it."
2. **GPT** executes 2.2 → 2.3 → 2.5 → 2.7 sequentially.
   - Drafts all sections with default values, then composes full.
   - Applies risk/privacy templates, redaction flags.
   - Uses Token Utility and Profile Engine.
   - Includes validations and checklists.

### Journey C: Review and Revise
1. **User** uploads external feedback.
   - **Tool**: 2.6 Feedback Tool.
2. **GPT** synthesizes comments and redlines sections.
   - Prompts again for clarifications or evidence.
3. **User** confirms or updates content.
4. **GPT** updates draft, logs changes, re-commits via 2.7.
   - Tracks metadata and approval history via 2.9.
