## Work Package Definitions (Phase 2 Updates)

### ✅ WP7 – Project Profile and Metadata Generation
**Updated Scope:**
- Generate, validate, and manage project-level metadata that supports downstream draft generation.
- Integrate with `ProjectProfile` schema from DB.
- Pre-fill inputs based on user context or uploads.
- Ensure metadata is linked to all gate/artifact drafts.

**Status:** Scope confirmed; no change needed.

---

### 🆕 WP17b – Draft Artifact Sections from Inputs
**New WP replacing/augmenting WP17 Prompt Patterns.**

**Scope:**
- Implement planner-triggered flow to convert user inputs (from `PromptLog`) into structured drafts for `ArtifactSection`.
- Leverage `compose_and_cite` and `searchKnowledgeBase` tools.
- Align to `dense_artifact_generation.md` design patch.
- Track outputs in `ReasoningTrace` and `ArtifactSection` tables.

**Includes:**
- Tool: `compose_and_cite`
- Input source: PromptLog (user inputs tagged by section + intent)
- Planner logic to detect readiness and generate draft.

**Links:**
- DB schema: `ArtifactSection`, `ReasoningTrace`
- Design: `dense_artifact_generation.md`

---

### 🆕 WP18 – Artifact Assembly and Routing
**Scope:**
- Stitch individual `ArtifactSection` entries into full artifacts.
- Log to `DocumentVersionLog`.
- Route for validation, feedback, Drive sync.

**Includes:**
- Diff check and versioning (`DocumentDiff`)
- Save metadata and approvals (`ApprovalLog`, `DocumentFeedback`)
- Final output to Google Drive

**Links:**
- DB schema: `DocumentVersionLog`, `AuditTrail`
- Design: `dense_artifact_generation.md`

---

### 🆕 WP20 – Google Drive Storage Integration
**Scope:**
- Push draft artifacts and sections to Drive.
- Store and maintain URLs in `google_doc_url`.
- Poll or webhook for edits and sync back.

**Includes:**
- Section-level export
- Version tracking in `DocumentVersionLog`

**Links:**
- Design: `dense_artifact_generation.md`

---

### 🆕 Spillover – Tool + Memory Enhancements
**Scope:**
- `queryCorpus`: Search tool for vector DB (Chroma)
- Update PromptLog model for richer session tracking
- Auto-snapshot and session summary tools
- Register all tools in tool manifest + catalog
- Improve `inputChecker` to use fuzzy or LLM-based evaluation
- Extend input pipeline to link with project profile fields

**Links:**
- DB schema: `PromptLog`, `ArtifactSection`, `ProjectProfile`

---

These definitions are now aligned with the `dense_artifact_generation.md` UX + technical flow and `db_schema_notes_v3.md` structure. Each WP now clearly owns a slice of the generation lifecycle from input to Drive-ready artifact.