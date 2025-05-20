## Master Data Flow (v2)

This document visualizes and explains the data flow architecture for the PolicyGPT system, from user interaction to document export. It reflects a planner-driven, session-backed flow with human-in-the-loop editing, reasoning traceability, and toolchain visibility.

---

### 🔁 High-Level Flow Overview

```
[User (GPT Chat)]
      ↓
[Planner: Create Task] --uses--> gate_reference.yaml
      ↓
[Session Memory Setup] ←→ [Drive + Airtable Reference Load]
      ↓
[Project Profile Loaded] ← project_profile.yaml (central fact base)
      ↓
[Compose + Validate Tools] --calls→ GPT, ChromaDB, Airtable, WebSearch
      ↓
[Section Output] --saved to→ ArtifactSection, ReasoningTrace
      ↓
[Human Review + Feedback] --captured in→ AuditTrail, PromptLog
      ↓
[Final Approval] --logged to→ DocumentVersionLog, Export
      ↓
[Document Assembly] ← collates → all `ArtifactSection` entries
      ↓
[Stakeholder Review] --feedback→ new task or version suggestion
      ↓
[Doc Feedback Processor] --logs to→ DocumentFeedback, DocumentDiff, ApprovalLog
```

---

### 🧠 Core Flows

#### 1. **Task Initialization**

* Input: user says "I want to generate documents for Gate 2"
* System:

  * Queries `gate_reference.yaml` for required artifacts
  * Stores `TaskMetadata` with section list and planner trace scaffold
  * Loads YAML memory snapshot if any from `/system/fetch_session`
  * Loads and caches `project_profile.yaml` (fact base for the project)

#### 2. **Drafting (GPT + Tools)**

* Planner picks section + toolchain
* GPT composes initial content using `compose_and_cite`
* If citation/logic fails, `validate_section` triggered
* Tools refer to project facts from `project_profile.yaml`
* Outputs are saved to `ArtifactSection`, reasoning path to `ReasoningTrace`

#### 3. **Human-in-the-Loop Review**

* GPT output presented back to user
* User can accept, edit, reject, or give feedback
* Edits update `ArtifactSection`
* Feedback logs to `AuditTrail`, `PromptLog`, `ReasoningTrace`

#### 4. **Version Commit + Export**

* Once approved, `commit_and_export` builds full document bundle (MD, HTML, PDF)
* Final version and metadata stored in `DocumentVersionLog`
* Export archive optionally synced to Drive or zipped via `/export/generate_bundle`

#### 5. **Document Assembly**

* The final document (e.g. Business Case or Project Charter) is composed by rolling up all validated `ArtifactSection` entries that match the selected `artifact_name` and `gate`
* Ordering is defined in `gate_reference.yaml`
* Final document is reviewed as a cohesive product before submission
* Project-wide context from `project_profile.yaml` ensures consistency across sections
* Document-level audit trace is logged in `DocumentVersionLog`

#### 6. **Stakeholder Feedback Loop**

* After assembly, the full document is distributed to reviewers/approvers
* Stakeholders can:

  * Provide holistic comments (e.g., consistency, tone, gaps)
  * Trigger new planning tasks (e.g., regenerate intro, clarify risk section)
  * Request a revision cycle tracked in `TaskMetadata`, with deltas stored in `AuditTrail` and `DocumentVersionLog`
* A new entry in `DocumentFeedback` and `DocumentDiff` is created for traceability
* If approved, `ApprovalLog` is updated

This loop allows alignment of section-by-section detail with whole-document clarity and quality before approval.

---

### 🗂️ Storage Map (Simplified)

| Data Object             | Stored In              | Trigger                                          |
| ----------------------- | ---------------------- | ------------------------------------------------ |
| Section Drafts          | `ArtifactSection`      | GPT `compose_and_cite`, user edit                |
| Planner Decisions       | `ReasoningTrace`       | During planner or validation flows               |
| GPT Logs                | `PromptLog`            | Every GPT call                                   |
| Audit Feedback          | `AuditTrail`           | User feedback or manual validation               |
| Output Versions         | `DocumentVersionLog`   | On commit/export trigger                         |
| Task Runtime Metadata   | `TaskMetadata`         | During initialization + planner execution        |
| Whole Document Feedback | `DocumentFeedback`     | Stakeholder or user comments on export           |
| Document Diffs          | `DocumentDiff`         | Tracked changes between exports                  |
| Document Approvals      | `ApprovalLog`          | Final stakeholder approval or rejection          |
| Project Fact Base       | `project_profile.yaml` | Loaded on task start, referenced during drafting |

---

### 🛠️ Example Toolchain (Section: Risk Management)

```
Plan: determine tools needed → [search_kb, query_airtable, compose_and_cite]
Run chain:
  - search_kb: finds prior risk registers
  - query_airtable: pulls org context
  - compose_and_cite: generates draft w/ inline references using project_profile
Validate:
  - validate_section: checks citation and fact flow
Review:
  - human approves, sends to commit
Export:
  - commit_and_export writes MD/PDF, logs version
Feedback:
  - reviewer provides holistic comments → document_feedback_tool
```

---

### 🔁 Iteration Cycle

At each section stage:

* Human can trigger re-run, force a tool, request simplification
* GPT logs updated prompt + citations
* Memory is optionally updated via `/system/sync_session_memory`

At document level:

* Feedback on full assembled document triggers one or more new `planner_tasks`
* Sections flagged for regeneration enter new review cycle
* All changes are logged and linked to the original `DocumentVersionLog`

---

### 📎 Clarification: Section-to-Document Flow

While the user and GPT work section-by-section (one slice of an artifact at a time), each `ArtifactSection` is tagged with its `artifact_name`, `section_name`, and `gate`.

At export time:

* All sections under a given `artifact_name` and `gate` are fetched
* They are ordered according to `gate_reference.yaml`
* Project-wide facts from `project_profile.yaml` are injected into final context
* The assembled document is rendered (e.g., `Business_Case_Gate2.pdf`) and presented to stakeholders for feedback and approval
* Stakeholders provide feedback on the document as a whole, enabling adjustments to framing, consistency, logic across sections, or tone

This staged, composable flow allows for distributed review and tight tracking of reasoning trace per section, while preserving auditability of the final assembled document.

---

### ✅ Actions to Complete

* [ ] Add fallback notes to each flow stage
* [ ] Add citation validation hook to export step
* [ ] Add visualization chart of planner-tool-human handoff
* [ ] Implement retry-visibility in PromptLog for GPT fallbacks
* [ ] Build feedback-to-revision loop for whole-document review
* [ ] Add API and tool for `document_feedback_tool`
* [ ] Add diff summarization and trace tracking to `DocumentDiff`
* [ ] Update UI or GPT frontend to support stakeholder comment injection
* [ ] Add `project_profile.yaml` schema and editing flow to DB and tools
