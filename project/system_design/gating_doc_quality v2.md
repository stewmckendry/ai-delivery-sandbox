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
