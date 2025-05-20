# PolicyGPT Acceptance Criteria

This document outlines the acceptance criteria for each core component of PolicyGPT. These criteria ensure each tool performs its intended function and meets quality, traceability, and usability standards.

---

## 1. Foundational Work Packages

### 1.1 Document and Metadata Reference Layer
- Queries by gate number return correct artifact list, templates, and requirements
- Each artifact entry includes:
  - Required fields
  - Example prompts
  - Acceptance checklist
- Users can preview structure/schema before use
- Changes in YAML update tools using reference data

### 1.2 Google Drive Integration
- Files successfully commit and return a Drive URL
- Metadata includes:
  - File type (section, full doc)
  - Gate number
  - Draft status
  - User ID
- Commit logs viewable by user
- Search retrieves previous submissions by metadata tag
- Users can fetch existing file contents from Drive
- Users can retrieve a list of files within specified folder(s)

### 1.3 YAML Project Profile Engine
- Profile is created or populated from user input
- Profile data is reused across all drafting tools
- User can edit profile inline or via upload
- Changes are reflected in generated text and summaries

### 1.4 Evidence and Alignment Search
- Given a section topic, evidence results return:
  - At least 3 citations with links
  - GC-alignment tags (e.g., policy priorities, mandates)
- User can see and select which citations to include
- Redundant or non-relevant evidence filtered out
- Returns relevant data or statistics, external research or studies, examples from other jurisdictions, and market scans
- For GC-specific searches, also returns previous GC projects and Auditor General reports

### 1.5 Token Count Utility
- Sections above 12k tokens trigger chunking
- Warnings shown to user when chunking applied
- Split sections preserve continuity and tone
- Tracks token count of the full GPT chat (prompts + responses) to monitor utilization and trigger scale-out as needed

---

## 2. Core User Tools

### 2.1 Artifact Lookup & Checklist Builder
- Inputs gate number → returns:
  - Artifact list
  - Submission checklist
  - Acceptance criteria
- Checklist visually differentiates required vs. optional

### 2.2 Input Ingestion & Summarizer
- Accepts file uploads (PDF, Word, Notes, etc.)
- Summarizes inputs into structured YAML
- Flags missing information (e.g., stakeholder data)
- Returns file preview and YAML view
- Includes prior artifacts from previous gates as inputs

### 2.3 Section Drafting Tool
- Uses guided questions if no input found
- Inserts evidence (from 1.4) when needed
- Drafts align with artifact schema from 1.1
- Validates required fields are filled before submission
- Supports bilingual mode (EN/FR toggle)
- Uses project profile to maintain tone, goals, etc.
- Drafts meet federal government quality standards: formal, thorough, and evidence-based
- Supports fetching latest section versions from Google Drive for editing

### 2.4 Section Iteration Engine
- Edits made in GPT canvas update underlying YAML
- Each edit tracked with user comment or approval
- Draft changes saved with timestamp and rationale
- Returns preview + metadata summary before commit
- Drafts meet formal tone, completeness, and accuracy expectations
- Fetches the latest committed section from Drive before updating

### 2.5 Full Document Composer
- Assembles all committed sections into ordered full document
- Inserts transition paragraphs where needed
- User can preview full document before final save
- Ensures consistent tone, terms, goals throughout
- Supports fetching all section content from Drive to ensure up-to-date composition

### 2.6 Feedback Ingestion Tool
- Accepts annotated PDFs, comments
- Maps feedback to relevant sections
- Suggests edits and highlights rationale
- Updates version in Drive, logs comment origin
- Updates applied to complete section drafts with formal tone
- Can retrieve the latest section for editing before changes

### 2.7 Export and Commit Tool
- Converts file to Word/PDF
- Attaches:
  - Version number
  - Draft/final label
  - Reviewer initials
  - Gate status
- Commits metadata to Drive, returns shareable link
- Commits full versions of documents without truncation or redaction
- Applies chunking when needed to handle large content sizes

### 2.8 Translation and Bilingual Tool
- User selects language: EN or FR
- Full document or per section translation
- Maintains formatting (headers, bullets)
- Returns translated doc with label
- Stores both EN and FR versions using Drive integration from 1.2 and export tool from 2.7

### 2.9 Version and Approval History Tracker
- Logs each commit with:
  - User ID
  - Timestamp
  - Gate status
- Users can view approval history (who, when, what changed)
- Provides direct links to signed versions