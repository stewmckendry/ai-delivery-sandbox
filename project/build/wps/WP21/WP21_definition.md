## WP21 – Spillover Tools and Memory Enhancements

### 🎯 Objective
Capture spillover scope from WP16 and other Phase 1 WPs to complete foundational tools and schema wiring. This includes embedding search, prompt logging, and manifest improvements.

### 📦 Scope of Work
**In Scope:**
- Build `queryCorpus` tool to search vector DB
- Enhance `inputChecker` to support LLM-based completeness checks
- Wire tools into GPT manifest and tool catalog
- Extend input pipeline to link with project profile fields
- Update PromptLog model for richer session tracking
- Auto-snapshot and session summary tools

**Out of Scope:**
- New UX or frontend features (Phase 3)
- Full section regeneration (handled by WP17b)

### 🚀 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/tools/tool_wrappers/queryCorpus.py` | Tool to query Chroma DB and return relevant chunks |
| `project/reference/tool_catalog.yaml` | Tool definitions with metadata schemas |
| `project/reference/gpt_tools_manifest.json` | Manifest for GPT integration |
| `app/db/models/PromptLog.py` | Schema updates for input/output paths or metadata blobs |

### ✅ Acceptance Criteria
- [ ] Tools registered and callable via API
- [ ] Schema validation prevents malformed inputs
- [ ] Memory logs retrievable by session or tag

### 🔗 Dependencies
- WP16 (tool wrappers, PromptLog)
- WP18 (tool call orchestration)

**Links:**
- DB schema: `PromptLog`, `ArtifactSection`, `ProjectProfile`

### 📥 Inputs
- Structured metadata (gate, artifact, section, intent)
- Queries from planner or GPT user

### 📤 Outputs
- Chroma DB matches
- Prompt validation results
- Updated schemas

### 🧠 Notes
- Enables robust memory querying and log review
- Bridges tools built in WP16 with upcoming planner flow