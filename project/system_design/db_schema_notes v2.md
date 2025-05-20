## Database Schema Notes (v2.2 - Planner-Traceable + Reasoning Aligned)

This file defines the long-term storage model for PolicyGPT. It captures core entities for artifact drafting, reasoning traceability, and audit readiness.

---

### 🧱 Core Tables and Purpose

| Table Name           | Description                                                             |
| -------------------- | ----------------------------------------------------------------------- |
| `ArtifactSection`    | Canonical source of truth for draft content, by gate/artifact/section   |
| `PromptLog`          | All GPT inputs/outputs for transparency and debugging                   |
| `ReasoningTrace`     | Serialized steps and decisions from planner and LLM                     |
| `DocumentVersionLog` | Versioning of full artifact drafts (PDF, HTML, Markdown, Drive link)    |
| `AuditTrail`         | Human + GPT actions (tool calls, validations, feedback) with timestamps |
| `TaskMetadata`       | Metadata for planner task runs (status, toolchain used, errors, etc.)   |

---

### 🧩 Schema Definitions (Core Entities)

#### `ArtifactSection`

```sql
artifact_section_id TEXT PRIMARY KEY
artifact_name TEXT
section_name TEXT
gate INT
content TEXT               -- working draft
validated BOOLEAN
template_id TEXT
example_id TEXT
google_doc_url TEXT        -- optional pointer to Drive-editable section
last_updated TIMESTAMP
```

#### `PromptLog`

```sql
prompt_log_id TEXT PRIMARY KEY
task_id TEXT
input TEXT
output TEXT
model_name TEXT
created_at TIMESTAMP
```

#### `ReasoningTrace`

```sql
trace_id TEXT PRIMARY KEY
section_id TEXT
steps JSONB  -- ordered list of reasoning steps
created_by TEXT
created_at TIMESTAMP
```

#### `DocumentVersionLog`

```sql
doc_version_id TEXT PRIMARY KEY
artifact_name TEXT
gate INT
version_tag TEXT
submitted_by TEXT
file_path TEXT
google_doc_url TEXT  -- optional Drive link to finalized artifact
doc_format TEXT       -- pdf/html/md
submitted_at TIMESTAMP
```

#### `AuditTrail`

```sql
audit_id TEXT PRIMARY KEY
user_id TEXT
action TEXT
entity_type TEXT
entity_id TEXT
metadata JSONB
timestamp TIMESTAMP
```

#### `TaskMetadata`

```sql
task_id TEXT PRIMARY KEY
artifact TEXT
section TEXT
gate INT
toolchain TEXT[]
status TEXT
errors TEXT[]
started_at TIMESTAMP
completed_at TIMESTAMP
```

## 🔧 Patch: Add DB Schema Entities for Document Feedback and Project-Level Logging

### 📌 Add New Table: `DocumentFeedback`

```sql
document_feedback_id TEXT PRIMARY KEY
document_id TEXT                      -- Foreign key to full document (e.g., artifact version or section group)
submitted_by TEXT
feedback_text TEXT
feedback_type TEXT                    -- e.g., 'usability', 'clarity', 'alignment', 'recommendation'
status TEXT                           -- e.g., 'open', 'in_progress', 'resolved'
linked_task_id TEXT                   -- Optional reference to auto-generated TaskMetadata
created_at TIMESTAMP
resolved_at TIMESTAMP
```

### 📌 Add New Table: DocumentDiff
```sql
diff_id TEXT PRIMARY KEY
document_id TEXT                      -- Target document version ID
previous_version_id TEXT             -- Comparison base
diff_summary TEXT                    -- Natural language or markdown diff
diff_type TEXT                       -- e.g., 'minor', 'major', 'formatting', 'structural'
generated_by TEXT                    -- GPT or Human
created_at TIMESTAMP
```

### 📌 Add New Table: ApprovalLog
```sql
approval_id TEXT PRIMARY KEY
document_id TEXT
approver_id TEXT
decision TEXT                        -- e.g., 'approved', 'rejected', 'approved_with_changes'
comments TEXT
signed_at TIMESTAMP
```

### 📌 Add New Table: ProjectProfile
```sql
project_id TEXT PRIMARY KEY
title TEXT
sponsor TEXT
project_type TEXT
total_budget NUMERIC
start_date DATE
end_date DATE
strategic_alignment TEXT
current_gate INT
last_updated TIMESTAMP
```

---

### 🗺️ Read/Write Scenarios (Usage Journeys)

| Scenario                 | Reads From                                                     | Writes To                                                                  |
| ------------------------ | -------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Planner runs for section | `gate_reference.yaml` to determine section needs               | `TaskMetadata` (initial plan), `ReasoningTrace` (initial steps scaffold)   |
| Draft composed           | `ArtifactSection.content`, `PromptLog.output` (prior examples) | `ArtifactSection.content`, `last_updated`; `PromptLog` (append new entry)  |
| Draft validated          | `ArtifactSection.content`, `ReasoningTrace.steps`              | `AuditTrail` (append: validation status, errors, reviewer)                 |
| Human feedback submitted | `ArtifactSection.content`, `PromptLog.input/output`            | `AuditTrail` (feedback entry), `ArtifactSection.validated = false`         |
| Final version committed  | `ArtifactSection.content`, `ReasoningTrace`                    | `DocumentVersionLog` (snapshot + Drive path), `AuditTrail` (commit action) |

### 🔄 Updates to Read/Write Scenarios

| Scenario                   | Reads From                                      | Writes To                     |
|----------------------------|-------------------------------------------------|-------------------------------|
| Document-level feedback    | DocumentVersionLog, ArtifactSection             | DocumentFeedback, AuditTrail |
| Version comparison triggered | DocumentVersionLog, ArtifactSection.content   | DocumentDiff                  |
| Reviewer sign-off          | DocumentVersionLog, ProjectProfile              | ApprovalLog                   |
| Project dashboard views    | ProjectProfile, AuditTrail, DocumentDiff        | N/A                           |

---


> 🔍 **Clarifications:**
>
> * **`ArtifactSection`** holds the working content. External editing (e.g. Google Docs) is optional and referenced via `google_doc_url`.
> * **Drive links** are not used for inline LLM reasoning — they serve as export destinations or editing surfaces.
> * **`DocumentVersionLog.google_doc_url`** enables traceability to externally shared versions, e.g. for approval processes.

---

### 🛠️ Implementation Actions

* [ ] Implement DB migrations for schema above (PostgreSQL preferred)
* [ ] Enable foreign key linking between section, trace, and version logs
* [ ] Create endpoints to query history by section, gate, or artifact
* [ ] Build admin dashboard to visualize reasoning lineage + draft history
* [ ] Auto-sync `ArtifactSection` and `DocumentVersionLog` with Drive backend
* [ ] Add logic to update `google_doc_url` fields upon Drive push/export
* [ ] Optional: Use webhooks or polling to detect edits in Drive and flag updates in `ArtifactSection`
- [ ] Create migration scripts for all new tables  
- [ ] Add linking logic between `DocumentVersionLog` and `DocumentFeedback`  
- [ ] Extend admin UI to show feedback, approval, and diff logs  
- [ ] Auto-generate tasks from feedback using `doc_feedback_to_task`  
- [ ] Enable gating logic to require `ApprovalLog` before artifact commit  
