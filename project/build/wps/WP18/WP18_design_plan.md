# WP18 – Artifact Assembly and Routing – Design Plan

## 🎯 Objective
Enable modular, traceable assembly of complete artifacts from section drafts, with validation, formatting, and routing to Drive.

## 🧭 PolicyGPT E2E Integration Context
This system enables the final assembly and delivery of multi-section artifacts within the end-to-end flow:
- Sections are drafted using the `generate_section` toolchain (WP17b)
- WP18 assembles the complete artifact using ordered section blocks
- Final artifact is routed for review and approval, and then stored to Drive (WP20)
- Outputs are accessible to users and GPT via markdown or rendered document previews

## 📦 Toolchain Overview
**Toolchain ID:** `assemble_artifact`

### Toolchain Steps
1. `load_section_metadata` – Fetch and sort ArtifactSection entries by gate using `gate_reference_v2.yaml`
2. `format_section` – Apply markdown/Jinja templates to structure section blocks
3. `merge_sections` – Combine formatted blocks into a complete markdown
4. `finalize_document` – Add TOC, title, metadata, trace, and prepare output

### Output
- Markdown and PDF versions of final artifact (business formal layout)
- `DocumentVersionLog` entry
- Logs to `ReasoningTrace`
- All tool calls logged to `PromptLog` using `log_tool_usage()`

## 🧱 Tools to Build
| Tool Name | Purpose | File |
|-----------|---------|------|
| load_section_metadata | Fetch + sort sections by artifact_id, gate_id | `tool_wrappers/loadSectionMetadata.py` |
| format_section | Apply formatting template | `tool_wrappers/formatSection.py` |
| merge_sections | Merge formatted blocks | `tool_wrappers/mergeSections.py` |
| finalize_document | Add header, TOC, finalize layout | `tool_wrappers/finalizeDocument.py` |
| commitArtifact | Store final output + trace | `tool_wrappers/commitArtifact.py` |

All tools conform to framework established in WP17:
- Each tool is a `Tool` class with `.run_tool()` and optional `validate()` methods
- Input/output schemas defined using Pydantic
- Tools registered and invoked using `tool_registry`

## 🧠 Data Models
- Input: `ArtifactSection` entries + `ReasoningTrace`
- Output: `DocumentVersionLog`
- Config: `gate_reference_v2.yaml`, artifact templates

## 📚 Templates
- Folder: `project/reference/artifact_templates/`
- Use Jinja or markdown blocks for reusable section formatting

## ✅ Acceptance Criteria
- Assembled artifact follows correct section order per gate
- Output markdown is valid and well-formatted
- Trace and version log are stored
- Optional draft chunk preview is supported
- GPT can fetch the complete artifact for user preview without hitting token/API limits (via streaming or summarization spec; implementation guide provided)
- Document spec includes Drive metadata structure for WP20 to consume

## 🔗 Planner Integration
- Toolchain registered in `planner_orchestrator.py`
- Triggered via `{ "intent": "assemble_artifact", "artifact_id": "...", "gate_id": 0 }`
- Use `generate_section_chain.py` as architectural reference

## 🧪 Test Plan
- CLI and API tests on Railway deployment: https://robust-adventure-production.up.railway.app
- Use test data from `project/test/WP17b/` or create new dummy data
- Validate all outputs: markdown structure, TOC, ReasoningTrace, version log
- Regression test for missing/optional fields

## 📘 Docs to Create
- WP18_template_reference.md
- WP18_gate_rendering_map.md
- User + API guides
- Guide for GPT-safe document fetching
- Spec for Google Drive handoff structure (for WP20)

## 🔄 Versioning Strategy
- Track version in `DocumentVersionLog`
- Link ReasoningTrace.id for each output
- Tag with toolchain + schema version

## 🚧 Risks
- Misalignment of section order or schema
- Tool output format drift
- Large artifacts exceeding token or storage limits

## 🪜 Next Steps
1. Confirm design plan with Human Lead
2. Build and test each tool
3. Register toolchain
4. Create sample test run with dummy data
5. Finalize documentation and integration hooks