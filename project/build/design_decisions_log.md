## Design Decisions Log

### 2025-05-22 — PromptLog Metadata Patch (from WP16)

**Decision:** Add a `metadata` column (JSON) to the `PromptLog` table

**Source:** `project/build/wps/WP16/PromptLog_metadata_patch.md`

**Purpose:**
To allow contextual tagging of each prompt with gate, artifact, section, and intent identifiers. This supports advanced filtering, traceability, and review workflows in downstream components.

**Impacted Components:**
- Database Schema: `PromptLog`
- Affected Tools: Any writing to `PromptLog` should now include metadata where relevant.
- Affected WPs: WP9 (memory ingest), WP4/WP6 (draft tools), WP7 (reasoning trace review), WP16 (input UI)

**Implications:**
- Tools must be updated to write this metadata.
- UI/Review layers can leverage this to group and filter prompts contextually.
- Enables stronger audit and QA mechanisms for documentation generation.

**Status:** ✅ Confirmed, to be implemented incrementally by responsible Pods.