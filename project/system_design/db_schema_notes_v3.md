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
artifact_section_id VARCHAR(36) PRIMARY KEY,
section_id VARCHAR(255),                     -- compound key artifact + section name
artifact_id VARCHAR(255),
gate_id VARCHAR(255),
text TEXT,                                   -- working draft content
sources TEXT,                                -- optional: list of citations/sources (JSON string)
status VARCHAR(50) DEFAULT 'draft',
generated_by VARCHAR(255),
timestamp DATETIME,
version VARCHAR(10) DEFAULT 'v1',
project_id VARCHAR(255)                      -- FK to project_profile(project_id)
```

#### `PromptLog`

```sql
id TEXT PRIMARY KEY,
tool TEXT,                                   -- Name of the tool used (e.g. inputPromptGenerator)
input_summary TEXT,                          -- Short summary of the input
output_summary TEXT,                         -- Short summary of the output
full_input_path TEXT,                        -- JSON path or blob storing full input data
full_output_path TEXT,                       -- JSON path or blob storing full output data
session_id TEXT,                             -- Optional: session ID for tracking
user_id TEXT,                                -- Optional: user ID for tracking
timestamp TIMESTAMP,
project_id VARCHAR(255)                      -- FK to project_profile(project_id)
```

Expected JSON structure inside full_input_path and full_output_path:
```json
{
  "input": {
    "gate": 0,
    "artifact": "investment_proposal_concept",
    "section": "problem_statement",
    "intent": "describe_problem",
    "answer": "..."
  }
}
```
#### `ReasoningTrace`

```sql
trace_id VARCHAR(36) PRIMARY KEY,
section_id VARCHAR(255),
steps NVARCHAR(MAX),                         -- ordered list of reasoning steps (JSON string)
created_by VARCHAR(255),
created_at DATETIME,
draft_chunks NVARCHAR(MAX),                  -- optional: store each draft section separately
project_id VARCHAR(255)                      -- FK to project_profile(project_id)
```

#### `DocumentVersionLog`

```sql
doc_version_id VARCHAR(255) PRIMARY KEY,
artifact_name TEXT NOT NULL,
gate INT NOT NULL,
version_tag VARCHAR(255) NOT NULL,
submitted_by VARCHAR(255),
file_path TEXT NOT NULL,
google_doc_url TEXT,                         -- optional Drive link to finalized artifact
doc_format VARCHAR(50) DEFAULT 'markdown',   -- pdf/html/md (default: markdown)
submitted_at DATETIME DEFAULT GETDATE(),     -- default: now()
project_id VARCHAR(255)                      -- FK to project_profile(project_id)
```

#### `ProjectProfile`

```sql
project_id VARCHAR(255) PRIMARY KEY,
title TEXT NOT NULL,
sponsor TEXT NULL,
project_type VARCHAR(255) NULL,
total_budget NUMERIC NULL,
start_date DATE NULL,
end_date DATE NULL,
strategic_alignment TEXT NULL,
current_gate INT NULL,
scope_summary TEXT NULL,
key_stakeholders TEXT NULL,
major_risks TEXT NULL,
resource_summary TEXT NULL,
last_updated DATETIME NOT NULL DEFAULT GETDATE()
```

#### `WebSearchLog`
```sql
id INTEGER PRIMARY KEY,
search_type VARCHAR,
query VARCHAR,
results_summary JSON,
tool_invoked_by VARCHAR,
user_id VARCHAR,
session_id VARCHAR,
project_id VARCHAR,                           -- disabled FK to project_profile(project_id) 
timestamp DATETIME
```


#### `AuditTrail`
(Not implemented)
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
(Not implemented)

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
(Not implemented)

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
(Not implemented)
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
(Not implemented)
```sql
approval_id TEXT PRIMARY KEY
document_id TEXT
approver_id TEXT
decision TEXT                        -- e.g., 'approved', 'rejected', 'approved_with_changes'
comments TEXT
signed_at TIMESTAMP
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
