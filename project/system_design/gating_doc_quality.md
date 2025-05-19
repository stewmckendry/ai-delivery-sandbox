---

## title: Gating Doc Quality

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

---

## Full-System Design Strategy

This approach applies guardrails and quality interventions across each layer of the PolicyGPT system.

---

## GPT User Prompting

**Strategy:** Prompts are structured to:
- Include formal language cues ("Generate a professional, evidence-based rationale..."),
- Incorporate structured user inputs (e.g. YAML-formatted stakeholder data),
- Invoke tools (e.g. EvidenceSearch) that improve factual grounding.

**Instruction Enforcement:** Prompt scaffolds define section-specific expectations (e.g. "Gate 0 Rationale section must reference strategic plan alignment...").

**Mitigations:**
- Prompt templates include fallback re-asks.
- Token estimator prevents overflow at prompt phase.

---

## GPT System Prompting / Config

**Location:** `policygpt_config.yaml`

**Instructions Embedded:**
- Target tone (professional, third-person)
- Target output length (min words, structured format)
- Required metadata (citations, reviewers, sources)
- Markdown formatting rules

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
```

---

## GPT Tools

**References:** `tool_catalog.md`, `api_contracts.md`

**Quality-Driven Tools:**
- `search_knowledge_base`: fetches evidence
- `compose_draft`: scaffolds content from YAML
- `revise_section`: edits iteratively, maintains structure
- `commit_document`: saves full artifact, validates YAML integrity

**Tool Behavior:** Tools validate required metadata before write (e.g. `commit_document` fails without `reviewers` list).

---

## FastAPI Backend Handling

**References:** `api_contracts.md`, `error_handling_matrix.md`

**Functions:**
- Token usage estimation (warn before overflow)
- PDF/Word rendering with WeasyPrint + Pandoc
- Metadata validation middleware
- Versioning enforcement on Drive + DB commit

---

## Database Schema for Metadata

**References:** `db_schema_notes.md`

**Tables Used:**
- `SectionDraft` — raw text + YAML metadata
- `PromptLog`, `ToolLog` — provenance tracking
- `AuditTrail` — commit time, approver, source links

**Sample Metadata Fields:**
- `reviewer_roles`
- `strategic_alignment`
- `section_origin_tool`
- `citation_sources`

---

## Error Handling

**References:** `error_handling_matrix.md`

**Common Failures + Responses:**
- Drive write error → fallback to local YAML + retry
- Tool validation failure → GPT prompt retry with user alert
- Token maxed → content chunked, partial save to DB

---

## Session Memory Model

**References:** `session_memory_model.md`

**Memory Design:**
- Mid-term: stores current draft + YAML
- Long-term: stores versions, approvals, audit logs

**Implementation:**
- `SessionState`, `SectionDraft`, `AuditTrail` tables
- YAML version used for fallback + GPT memory

---

## Integration Points

**References:** `integration_points.md`

**Google Drive:**
- Used for final committed artifact
- Users can open link in Google Docs for large edits
- Commit flow syncs changes back to Drive (bi-directional planned)

**Fallback Message Example:**
> "This section exceeds edit limit in chat. Please continue editing in Google Docs at this link..."

**Other Integrations:**
- ChromaDB for precedent retrieval
- Airtable for reference tables

---

## Additional Tactics

**1. Chunking:**
- Drafts are segmented into paragraphs, headers, YAML blocks for piecewise save + regenerate.

**2. Human-in-the-loop Required Fields:**
- E.g., project risks, costing data must be manually filled.

**3. YAML Backbone:**
- Source mapping + section metadata are written in YAML and saved with draft, ensuring re-reads use correct prior context.

**4. Output Format Rigidness:**
- Markdown structures enforced via validators before save (e.g., all bullets under "alternatives" must be rendered).

---

## New Design Additions

| Addition                                  | Justification                                               |
|------------------------------------------|-------------------------------------------------------------|
| `policygpt_config.yaml` with quality rules | Centralizes generation control for maintainability          |
| Metadata validators on commit            | Prevents half-baked outputs entering Drive or DB            |
| Token estimator on draft tools           | Avoids truncation mid-prompt or commit failures             |
| Drive fallback with editable link        | Ensures user can continue without loss when GPT overflows   |

---

## Summary

This document consolidates and extends system design to guarantee document outputs from PolicyGPT are high quality, auditable, and gate-ready. The implementation patterns detailed herein should be directly used during build and validated during PoC testing.

---