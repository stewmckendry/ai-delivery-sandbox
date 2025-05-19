---
title: DB Schema Notes
---

## Overview
This document defines the data models used within the PolicyGPT platform, with rationales for each entity and field. It supports the needs outlined in the user journeys, features, and acceptance criteria.

## Entities and Fields

### 1. ProjectProfile
- **Fields:**
  - `project_id` (UUID)
  - `title` (string)
  - `description` (string)
  - `gate_stage` (enum: Gate0, Gate1, ...)
  - `owner_id` (string)
  - `status` (enum: active, draft, finalized)
  - `last_updated` (timestamp)
- **Purpose:** Anchor object for all draft artifacts and user sessions.

### 2. ArtifactSection
- **Fields:**
  - `section_id` (UUID)
  - `project_id` (foreign key)
  - `section_type` (e.g., Rationale, Outcomes, RiskSummary)
  - `content_markdown` (text)
  - `draft_status` (enum: draft, revised, final)
  - `last_editor` (userID)
  - `reviewer_initials` (string)
  - `gate_stage` (enum)
  - `version` (integer)
  - `created_at`, `updated_at` (timestamps)
- **Purpose:** Draft content unit linked to a project and used in composition.

### 3. ArtifactDocument
- **Fields:**
  - `document_id` (UUID)
  - `project_id` (foreign key)
  - `title` (string)
  - `document_type` (enum: PDF, Word, GDoc)
  - `language` (enum: EN, FR)
  - `drive_url` (string)
  - `commit_user` (userID)
  - `commit_notes` (text)
  - `commit_date` (timestamp)
- **Purpose:** Assembled output committed to Google Drive.

### 4. PromptLog
- **Fields:**
  - `prompt_id` (UUID)
  - `session_id` (UUID)
  - `project_id`, `section_id` (foreign keys)
  - `prompt_text`, `response_text` (text)
  - `timestamp`
- **Purpose:** Stores GPT interactions for audit and debugging.

### 5. FileMetadata
- **Fields:**
  - `file_id` (UUID)
  - `project_id` (foreign key)
  - `filename` (string)
  - `file_type` (enum: docx, pdf, yaml, md, csv)
  - `source` (user_upload, gpt_generated, google_drive)
  - `ingest_status` (enum: parsed, failed, skipped)
  - `metadata_blob` (json)
- **Purpose:** Track inputs and parsed results from uploaded or linked files.

## Where These Entities Are Stored
- All entities are stored in a **PostgreSQL** relational database managed by the backend (FastAPI).
- Indexes are used on `project_id`, `section_type`, and `gate_stage` to support fast lookups.
- Vector embeddings (e.g., from content_markdown) are stored separately in **ChromaDB** for semantic search.
- YAML versions of ProjectProfile and ArtifactSection are serialized for GPT memory scaffolding.
- Redundant copies of final documents and logs are also stored in **Google Drive** for user-facing access.

## Example Use Case: Gate 0 Initiation

### Step 1: User starts a Gate 0 draft (Journey A)
- **ProjectProfile** is created with metadata: title, gate_stage="Gate0", owner_id.

### Step 2: User uploads input files
- **FileMetadata** entries are created per file.
- Files are parsed, and YAML summaries update the **ProjectProfile**.

### Step 3: GPT generates a draft section (e.g., Rationale)
- **ArtifactSection** is created with content_markdown and section_type="Rationale".
- Metadata includes gate_stage="Gate0", draft_status="draft".

### Step 4: User iterates on draft in Canvas
- **PromptLog** stores each GPT prompt/response pair.
- **ArtifactSection** is updated on every commitSection call.

### Step 5: User finalizes the Gate 0 document
- Sections are composed into **ArtifactDocument**.
- File is committed to Drive, with metadata including reviewerInitials, gate_stage, version.

## Next Steps
- Visual ER diagram
- Sample queries (SQL + FastAPI)
- Versioning support per schema