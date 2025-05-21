## Tool Catalog (Enhanced)

### Overview

This catalog defines the full suite of tools available to the PolicyGPT system, aligned with an evidence-first, traceable drafting workflow. Each tool includes its function, input/output schema, validation logic, chaining context, and role in the AI reasoning trace.

---

## Core Tool Inventory

### 1. `compose_and_cite`

* **Function:** Orchestrates evidence search → synthesis → draft → validate.
* **Inputs:** `section_type`, `project_id`, `gate_stage`, optional `manual_inputs`
* **Outputs:** Validated section markdown + reasoning trace + citations
* **Notes:** Main path for section drafting; uses `searchKnowledgeBase`, `externalWebSearch`, `composeDraft`, `validateSection` under the hood.

### 2. `searchKnowledgeBase`

* **Function:** Retrieves semantic matches from embedded documents.
* **Inputs:** `query`, `tags` (e.g. gateStage, artifactType)
* **Outputs:** Ranked excerpts + doc metadata
* **Chaining Context:** Invoked from planner or `compose_and_cite`

### 3. `externalWebSearch`

* **Function:** Pulls evidence from trusted web sources
* **Inputs:** `query`, optional filters
* **Outputs:** Ranked links, snippets, credibility score
* **Chaining Context:** Fallback for low internal KB coverage

### 4. `composeDraft`

* **Function:** Generates structured markdown from YAML + evidence
* **Inputs:** YAML section fields, evidence summary
* **Outputs:** Draft markdown
* **Chaining Context:** Step 3 in `compose_and_cite`

### 5. `validateSection`

* **Function:** Validates presence of required fields and logic structure
* **Inputs:** `section_markdown`, `section_type`, `gate_stage`
* **Outputs:** Validator pass/fail, list of issues, formatted validator log
* **Chaining Context:** Always invoked before commit

### 6. `logReasoningTrace`

* **Function:** Stores reasoning trace for each toolchain run
* **Inputs:** `task_id`, `steps[]`, `inputs`, `outputs`, `citations`
* **Outputs:** YAML + DB entry
* **Chaining Context:** Final step in planner sequence

### 7. `commitSection`

* **Function:** Saves validated section to Google Drive and DB
* **Inputs:** `project_id`, `section_type`, `content`, `language`, `version`, `reviewer_initials`
* **Outputs:** Drive link, DB update to `ArtifactSection`
* **Preconditions:** Must be validated via `validateSection`

### 8. `commitDocument`

* **Function:** Assembles and stores full artifact
* **Inputs:** `section_ids[]`, `title`, `language`, `version`, `gate_stage`
* **Outputs:** Google Doc + PDF + DB entry
* **Chaining Context:** Triggered after section plan complete

### 9. `fetchDocument`

* **Function:** Retrieves section or full document
* **Inputs:** `section_id` or `document_id`
* **Outputs:** Markdown, Word, or PDF version

### 10. `getTokenUsage`

* **Function:** Tracks GPT session size and warns on overflow
* **Inputs:** `session_id` or `text`
* **Outputs:** Token count, % used

### 11. `translateDocument`

* **Function:** Converts document language (EN ⇆ FR)
* **Inputs:** Markdown
* **Outputs:** Translated Markdown

### 12. `queryAirtable`

* **Function:** Looks up structured reference mappings (risk indicators, cost precedents)
* **Inputs:** `table_name`, `filters`
* **Outputs:** JSON records

### 13. `parseTranscript`

* **Function:** Converts .txt or .docx transcripts to YAML insights
* **Inputs:** File upload
* **Outputs:** YAML summary for project inputs

### 14. `loadCorpus`

* **Function:** Embeds and indexes new documents into KB
* **Inputs:** File (PDF, DOCX)
* **Outputs:** Vectorized record + refresh log

### 15. `doc_feedback_to_task`

* **Function:** Converts full-document feedback into new planner tasks or edits
* **Inputs:** `document_id`, `feedback_text`, optional `feedback_type`
* **Outputs:** Suggested edits or tasks (YAML task format)
* **Use Case:** Enables post-review updates or planning retries

### 16. `diff_and_summarize_sections`

* **Function:** Computes section-level diffs and summarizes key changes
* **Inputs:** `old_content`, `new_content`, `section_type`
* **Outputs:** Structured diff summary + optional changelog snippet
* **Use Case:** Version tracking, approval workflows, audit logs

### 17. `submitDocumentFeedback`

* **Function:** Captures user-level feedback on document drafts
* **Inputs:** `document_id`, `feedback_text`, `user_id`, `feedback_type`, `timestamp`
* **Outputs:** Logged feedback entry
* **Chaining Context:** Can trigger `doc_feedback_to_task` or planner retries
* **Notes:** Stored in `DocumentFeedback` table for traceability

### 18. `summarize_feedback_log`

* **Function:** Synthesizes all feedback entries for a document
* **Inputs:** `document_id`
* **Outputs:** Summary of themes, suggested actions
* **Use Case:** Planner review, coordination with approvers

---

## Tool Catalog Addendum (WP9 Ingestion Tools)

### 19. `uploadTextInput`
* **Function:** Logs user-entered freeform text into memory + DB
* **Inputs:** `text` string
* **Outputs:** YAML summary (written to `logs/ingest_traces/`), DB entry (PromptLog)
* **Validation:** Requires non-empty text, max 10k characters
* **Notes:** Used for analyst paste-in or planner-triggered inputs

### 20. `uploadFileInput`
* **Function:** Extracts and logs file-based input (PDF, DOCX)
* **Inputs:** File path
* **Outputs:** YAML trace + DB entry
* **Validation:** Checks file readability and valid extension
* **Notes:** Supports bulk ingestion of reports or articles

### 21. `uploadLinkInput`
* **Function:** Pulls and logs web-based content from a given URL
* **Inputs:** URL string
* **Outputs:** YAML trace + DB log
* **Validation:** Valid URL, must contain parseable body text
* **Notes:** Used for sourcing from trusted web domains

### 22. `createSessionSnapshot`
* **Function:** Saves a structured memory summary for session handoff
* **Inputs:** Session ID, tags, memory blob
* **Outputs:** Snapshot record (SessionSnapshot DB)
* **Validation:** Requires session context
* **Notes:** Enables planner recall or downstream tool reuse

---

## 🔁 Updated Enhancements Summary (with additions)

| Tool                     | Enhancement                                             |
|--------------------------|----------------------------------------------------------|
| `compose_and_cite`       | Enables tool chaining + validation checkpoint            |
| `validateSection`        | Enforces structure, completeness, traceability           |
| `logReasoningTrace`      | Adds provenance record per drafting sequence             |
| `commitSection`          | Requires validation before write                         |
| `searchKnowledgeBase`    | Tied to planner search intent                            |
| `doc_feedback_to_task`   | Adds feedback-driven revision planning                   |
| `diff_and_summarize_sections` | Enables section-level diff tracking for audit           |
| `submitDocumentFeedback` | Captures user feedback at document level                 |
| `summarize_feedback_log` | Aggregates feedback to guide future edits or reviews     |

---

## Toolchain Flow Example (Gate 1: Rationale)

1. Planner triggers `compose_and_cite`
2. System queries KB via `searchKnowledgeBase`
3. Fallback if needed to `externalWebSearch`
4. GPT generates via `composeDraft`
5. Human reviews and edits the draft in Canvas or Docs
6. `validateSection` checks structure and completeness
7. If issues are found, GPT proposes fixes or user is prompted
8. `logReasoningTrace` records decisions, edits, and validation state
9. `commitSection` stores result once validated

---

This tool catalog supports end-to-end document drafting with integrity, reuse, and traceability—aligned with GC expectations and audit requirements.
