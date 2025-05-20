## Session Memory Model (v2.1 - Deep Research Enhanced)

This model governs how PolicyGPT handles memory at different time horizons, enabling reusable reasoning, validator traceability, and planning persistence.

---

### 🧠 Memory Layers

#### 1. Short-Term Memory (GPT Session)

* **Scope:** Single GPT session (token window + custom GPT memory)
* **Used For:** Inline thought chaining, search recall, follow-up generation
* **Storage:** Volatile, runtime only (not persisted)
* **Scaling:** Once token limits are hit or session slows, the planner rehydrates using mid-term memory.

#### 2. Mid-Term Memory (Task Scoped)

* **Scope:** Single user prompt or document section (e.g., "draft Gate 1 rationale")

* **Storage:** YAML + DB

* **Files:**

  * `reasoning_trace.yaml`: LLM-generated thoughts, tool calls, decisions
  * `planner_task_trace.yaml`: Step-by-step toolchain plan
  * `validation_log.yaml`: Output of `validateSection` and user feedback

* **Used For:** Rehydrating context between sessions, planner memory, trace export

* **Accessed During:**

  * Draft regeneration (`composeDraft`)
  * Section validation
  * Human feedback review

#### 3. Long-Term Memory (Project Scoped)

* **Scope:** Across gates and artifact versions
* **Storage:** Database + Google Drive
* **Tables / Entities:**

  * `ArtifactSection`: Canonical content
  * `PromptLog`: Raw GPT inputs/outputs
  * `ReasoningTrace`: Section provenance
  * `DocumentVersionLog`: Versioned submission history

---

### 🔄 New Clarifications: Memory Continuation Logic

#### Cross-Session Memory Rehydration

| Use Case                        | Source Layer        | Memory Retrieved                     |
|--------------------------------|---------------------|--------------------------------------|
| User returns after a break     | Mid-Term + Long-Term| `reasoning_trace.yaml`, last `PromptLog`, `ArtifactSection` content |
| Planner re-run after session end | Mid-Term           | `planner_task_trace.yaml`, `validation_log.yaml` |
| Full-document revision         | Long-Term           | All `ArtifactSection` content, `DocumentVersionLog`, `DocumentFeedback` |

---

### 🧠 Session Memory Bootstrap Logic

```yaml
on_session_start:
  if prior_section_draft exists:
    load reasoning_trace.yaml
    load planner_task_trace.yaml
    load validation_log.yaml
  else if prior_document_version exists:
    load latest DocumentVersionLog
    load all related ArtifactSection entries
  else:
    start fresh planner sequence
```
---

### 🗂️ Memory Schema (Mid-Term YAMLs)

#### `reasoning_trace.yaml`

```yaml
section_id: rationale-gate1
steps:
  - type: search
    tool: searchKnowledgeBase
    inputs: { query: ... }
    outputs: { passages: [...] }
  - type: generate
    tool: composeDraft
    reasoning: "..."
    citations: [...]
    outputs: { text: ... }
```

#### `planner_task_trace.yaml`

```yaml
section_id: rationale-gate1
plan:
  - searchKnowledgeBase
  - externalWebSearch
  - composeDraft
  - validateSection
  - commitSection
```

#### `validation_log.yaml`

```yaml
section_id: rationale-gate1
required_fields:
  - strategic_alignment: passed
  - evidence_basis: failed
notes: "Evidence weak. Needs stronger citation."
```

---

### 🔁 Read/Write Journeys

| Trigger           | Reads from                                  | Writes to                           |
| ----------------- | ------------------------------------------- | ----------------------------------- |
| `composeDraft`    | planner\_task\_trace.yaml                   | reasoning\_trace.yaml               |
| `validateSection` | gate\_reference.yaml, Artifact              | validation\_log.yaml                |
| Human edits       | ArtifactSection                             | validation\_log.yaml                |
| Planner rerun     | planner\_task\_trace.yaml                   | reasoning\_trace.yaml               |
| Final commit      | reasoning\_trace.yaml, validation\_log.yaml | ArtifactSection, DocumentVersionLog |

---

### 🛠️ Implementation Actions

* [ ] Enforce schema above for YAML exports
* [ ] Add versioning metadata (e.g., trace\_id, created\_by, timestamp)
* [ ] Expose `reasoning_trace.yaml` in UI for human review
* [ ] Enable "resume from trace" in planner
* [ ] Add search endpoint over `reasoning_trace.yaml` for reuse across gates
* [ ] Detect prior planner runs and pre-fill memory when `section_id` or `document_id` is reused  
* [ ] Enable planner to switch between "fresh", "rehydrated", and "full document" memory modes  
* [ ] Auto-link memory objects in `AuditTrail` for traceability across sessions
