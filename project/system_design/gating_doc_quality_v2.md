## title: Gating Doc Quality (Enhanced)

## Purpose

This document defines the full-system design approach required to reliably generate, edit, and finalize complex documentation that meets the quality bar for Government of Canada gating approvals. The approach is grounded in alignment with enterprise expectations around traceability, auditability, rigor, and language professionalism. It draws from and integrates all relevant system design artifacts.

---

## Quality Challenges to Solve

1. **Over-summarization**: Loss of fidelity in GPT outputs
2. **Informal tone**: Insufficient alignment with professional/government language
3. **Token limitations**: Truncated drafts or lost edits due to overflow
4. **Hallucination**: Outputs unsupported by evidence or precedent
5. **Re-generation inconsistency**: Loss of prior user edits or decisions
6. **Traceability gaps**: Lack of metadata to validate citations, sources, reviewers
7. **Output format issues**: Incomplete documents, misformatted outputs
8. **Disconnected narrative**: Lack of coherence across sections in long artifacts
9. **Lack of structured reasoning trace**: No record of GPT's rationale or logic steps

---

## Full-System Design Strategy

This approach applies guardrails and quality interventions across each layer of the PolicyGPT system.

---

## GPT User Prompting

**Strategy:** Prompts are structured to:

* Include formal language cues ("Generate a professional, evidence-based rationale..."),
* Incorporate structured user inputs (e.g. YAML-formatted stakeholder data),
* Invoke tools (e.g. EvidenceSearch) that improve factual grounding.

**Instruction Enforcement:** Prompt scaffolds define section-specific expectations (e.g. "Gate 0 Rationale section must reference strategic plan alignment...").

**Mitigations:**

* Prompt templates include fallback re-asks.
* Token estimator prevents overflow at prompt phase.

---

## GPT System Prompting / Config

**Location:** `policygpt_config.yaml`

**Instructions Embedded:**

* Target tone (professional, third-person)
* Target output length (min words, structured format)
* Required metadata (citations, reviewers, sources)
* Markdown formatting rules

**Enhancement:** Introduce `planner_enabled: true` and `quality_validator: enabled` to config file for agentic planning and validation enforcement.

**Example:**

```yaml
section_prompt:
  rationale:
    style: formal
    required_fields:
      - strategic_alignment
      - public_value
      - alternatives_considered
    length: ">= 600 words"
    citations: true
planner_enabled: true
quality_validator: enabled
```

---

## GPT Tools

**References:** `tool_catalog.md`, `api_contracts.md`

**Quality-Driven Tools:**

* `search_knowledge_base`: fetches evidence
* `external_web_search`: expands citation base
* `compose_draft`: scaffolds content from YAML
* `revise_section`: edits iteratively, maintains structure
* `commit_document`: saves full artifact, validates YAML integrity
* `get_token_usage`: estimates overflow risk
* `validate_section`: checks required fields, format, narrative trace
* `log_reasoning_trace`: stores structured rationale

**Enhancements:**

* Introduce `compose_and_cite`: a wrapper chain that invokes search > synthesize > draft > validate. This tool manages multi-step generation by automatically chaining evidence retrieval, synthesis, section drafting, and post-generation validation. It ensures outputs are aligned with gate reference expectations and are ready for commit without human intervention.
* Enforce validator gating before `commitSection` to ensure only validated and complete sections are accepted into the database and document chain.

---

## Agentic Planning and Orchestration

**New Component:** `document_orchestrator`

* Builds document plan by parsing project YAML and aligning requirements from `gate_reference.yaml`
* Uses `required_fields`, `section_types`, and `gate_stage` attributes to generate a sequenced task plan
* Dynamically invokes tools (`searchKnowledgeBase`, `composeDraft`, `validateSection`) per section based on planning logic
* Aligns content across sections by linking related rationale, alignment statements, and reviewer concerns

**Planner Log:** Records tool steps, inputs used, decisions made, and rationales in `reasoning_trace.yaml` for transparency and audit.

---

## FastAPI Backend Handling

**Functions:**

* Token usage estimation (warn before overflow)
* Validator enforcement before commit
* PDF/Word rendering with WeasyPrint + Pandoc
* Reasoning trace and validator logs per document
* Versioning enforcement on Drive + DB commit

---

## Database Schema for Metadata

**Tables Used:**

* `SectionDraft` — raw text + YAML metadata
* `PromptLog`, `ToolLog`, `ReasoningTrace` — provenance and logic tracking
* `AuditTrail` — commit time, approver, source links

**New Fields Proposed:**

* `reasoning_steps`
* `section_validator_passed`
* `planner_task_id`

**Schema Diagram Overview:**

| Table          | Field                      | Description                                                        |
| -------------- | -------------------------- | ------------------------------------------------------------------ |
| SectionDraft   | planner\_task\_id          | Link to the orchestration step that generated the section          |
| SectionDraft   | reasoning\_steps           | Serialized rationale summary per draft version                     |
| SectionDraft   | section\_validator\_passed | Boolean flag indicating if the section passed automated validation |
| ReasoningTrace | task\_id                   | Identifier for the planned subtask or draft component              |
| ReasoningTrace | steps\[]                   | Ordered list of reasoning actions taken during drafting            |
| AuditTrail     | source\_link               | Reference back to planner or validator output log                  |

This schema ensures that each generated section is traceable, testable, and linked to its planning context for audit or re-generation workflows.

---

## Error Handling

**Failure Scenarios + Responses:**

* Drive write error → fallback to local YAML + retry
* Validator failure → GPT retries revision with warning
* Token maxed → chunk content, save partial, queue continuation

---

## Session Memory Model

**Memory Design:**

* Mid-term: stores current draft + YAML
* Long-term: stores versions, approvals, audit logs, planner traces

**Enhancements:**

* Load reasoning trace and plan into GPT context on restart
* Store planner outline and decisions in YAML format

---

## Integration Points

**Google Drive:**

* Drive stores canonical document and log artifacts
* Users edit large sections externally; edits sync with YAML

**Other Integrations:**

* ChromaDB: policy embedding search
* Airtable: gate metadata, indicator tables
* Reasoning trace: stored in DB and downloadable as YAML/Markdown

---

## Additional Tactics

1. **Chunking:** Sections split for incremental edit/save.
2. **Inline Citation Enforcement:** Markdown includes source links inline.
3. **Human-in-the-loop Fields:** Required inputs prompted or flagged.
4. **Orchestrated Regeneration:** Revisions driven by planner feedback.
5. **Quality Validators:** Rule-based checker for logic + formatting + required fields.
6. **YAML Backbone:** Source mapping + validator rules embedded in YAML for reuse.

---

## New Design Additions

| Addition                               | Justification                                             |
| -------------------------------------- | --------------------------------------------------------- |
| `document_orchestrator` tool           | Enables full-document planning and narrative cohesion     |
| `validate_section` tool                | Quality gate before commit, flags missing fields          |
| `log_reasoning_trace` tool             | Enables auditability of AI reasoning                      |
| `compose_and_cite` tool wrapper        | Implements evidence → synthesis → draft in a single chain |
| Inline citation formatting             | Strengthens source traceability                           |
| Section-to-document consistency checks | Ensures cohesion and avoids contradictory outputs         |

---

## Summary

This enhanced system design integrates planning, validation, and traceability improvements to ensure that PolicyGPT outputs meet the Deep Research standard for evidence-based, coherent, auditable documents. Each enhancement supports the audit, quality, and usability goals expected of high-stakes government gating documentation.

---

# PATCH: Gating Doc Quality (v2.3 – Full Document + Feedback Loop Support) 

## 🔄 Enhancements for Document-Level Feedback and Approval

To support document-level feedback and gate approvals, the system introduces:

### 🔧 New Tools

* `diff_and_summarize_sections`: Compares prior and current versions to highlight key changes for reviewers.
* `doc_feedback_to_task`: Parses human feedback into planner-ready regeneration tasks.
* `record_approval_decision`: Logs reviewer sign-off, linking to specific version and rationale.

These tools work together to ensure comments are addressed and the planner reuses reviewer context in follow-up revisions.

---

### ✅ New Database Support

Schema enhancements enable end-to-end feedback and approval tracking:

| Table            | Field / Relation            | Purpose                                                |
| ---------------- | --------------------------- | ------------------------------------------------------ |
| `DocumentFeedback` | `doc_version_id`, `comments`, `reviewer_id`, `section_id`, `resolved` | Captures structured feedback tied to a document or section |
| `ApprovalLog`      | `doc_version_id`, `approver_id`, `decision`, `timestamp`, `comments` | Tracks formal reviewer sign-off for versioned artifacts |
| `DocumentDiff`     | `old_version_id`, `new_version_id`, `diff_text`, `summary`           | Captures high-level diffs for reviewer context          |

These logs are referenced in `AuditTrail` and surfaced in UI dashboards.

---

### 🧠 Planner Integration

Planner adjusts to handle:

- **Feedback-based Regeneration:** Tasks created from `DocumentFeedback` records guide selective redrafting.
- **Approval Gatekeeping:** `commitDocument` now checks for required approvals before finalization.
- **Full Document Reasoning Trace:** Planner logs span multiple sections, allowing reviewers to trace logic across artifact boundaries.

---

### 🗂️ Session Memory Extension

Memory model now stores and rehydrates:

- Prior `DocumentDiff` summaries for GPT context
- Unresolved feedback for follow-up drafts
- `ApprovalLog` state to determine gating readiness

---

### 📄 New Quality Control Checks

| Check                         | Trigger              | Tool Used                  |
| ---------------------------- | -------------------- | -------------------------- |
| Required fields present      | Before commit        | `validate_section`         |
| Feedback fully resolved      | On commit attempt    | `doc_feedback_to_task`     |
| Reviewer approval present    | On commit            | `record_approval_decision` |
| Narrative consistency across sections | On document compose | `document_orchestrator`     |

---

### ✨ Additional Design Tactics

* Flag unresolved feedback in UI before commit
* Embed approval status in YAML headers (e.g. `status: approved`, `approved_by:`)
* Visualize diffs for reviewers inside Drive or export PDF

---

These additions ensure PolicyGPT is capable of handling real-world gate review cycles—enabling high-quality, reviewable documents with minimal rework and maximum transparency.
