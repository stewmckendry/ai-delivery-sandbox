# WP24 Toolchain Plan: `generate_full_artifact_chain`

## 🎯 Objective
Build the `generate_full_artifact_chain` toolchain to automate full artifact creation, integrating planning, section generation, assembly, and logging.

---

## 🧱 Toolchain Responsibilities

| Step | Function | Tool(s) Involved |
|------|----------|------------------|
| 1. Plan Sections | Enumerate required sections | `gate_reference_v2.yaml` (fetched via raw GitHub) |
| 2. Iterate Sections | Run `generate_section_chain` for each section | `generate_section_chain` |
| 3. Section Context Memory | Provide summary of prior section(s) to each generation call | Inline context summary per step |
| 4. Logging | Log trace per section + task metadata | `ReasoningTrace`, `PromptLog`, `TaskMetadata` (new) |
| 5. Assemble Draft | Merge + finalize into document | `assemble_artifact_chain` |
| 6. Refine Final Output | Global doc polish step for consistency | `refine_document_chain` (TBD) |
| 7. Export | Upload to Drive, record in DB | `storeToDrive`, `DocumentVersionLog` |

---

## 🧭 User Journey Entry Points

| Scenario | Trigger | Inputs Assumed |
|----------|---------|----------------|
| Quick Draft | GPT + User selects "generate full artifact" | Inputs preloaded via `IngestInputChain` |
| Planner Mode | GPT assembles section list from gate | Project profile + context present |

---

## 🧾 User Journey Exit Pathways

| Output | Stored In | Purpose |
|--------|-----------|---------|
| Final Document (PDF) | Google Drive via `storeToDrive` | User receives link |
| Draft Sections | `ArtifactSection` | Revision support |
| Reasoning Steps | `ReasoningTrace` | GPT explainer, audit |
| Prompt Logs | `PromptLog` | Tune prompts, feedback |
| Task Summary | `TaskMetadata` (new) | Task completion + error capture |

---

## 📤 Outputs
- Markdown doc uploaded to Drive
- Trace logs (steps, draft chunks)
- Reasoning summary (per section + final)
- Task status (complete/failed)

---

## ⚙️ Technical Design

- Fetch `gate_reference_v2.yaml` from GitHub raw URL
- For each section:
  - Summarize prior sections
  - Check token usage → summarize if needed
  - Run `generate_section_chain`
  - Retry up to 3 times on failure
- Finalize: merge sections, format, refine document
- Commit output and logs to Drive + DB

---

## 🔁 Retry + Error Hooks
- 3 max retries per section (exponential backoff)
- Use `get_token_usage` + summarizer before LLM call
- Log failures to `TaskMetadata`

---

## 🧪 Test Plan (WP24)
- Full test: sample gate (Risk Plan), 3 sections
- Expect:
  - Valid markdown
  - Reasoning + prompt logs
  - Drive link stored

---

## 📁 Files to Create or Update
| File | Purpose |
|------|---------|
| `generate_full_artifact_chain.py` | Main orchestration logic |
| `refine_document_chain.py` | Global doc polish step |
| `test_generate_full_artifact.py` | Validation suite |
| `full_artifact_generation.yaml` | Planner logic prompt |
| `TaskMetadata.py` | New model: logs toolchain status/errors |
| `task_metadata.sql` | SQL table create statement |

---

## 🔗 Tool Registry Additions
- Add toolchain to `tool_catalog.yaml` + `gpt_tools_manifest.json`

---

## 🧠 Token Management Strategy
- Estimate tokens per section with `get_token_usage`
- Summarize memory if overflow risk detected
- Use summarizer between sections to reduce carryover

---

## 🤝 Dependencies & Assumptions
- Inputs preloaded via `IngestInputChain`
- Section metadata in `gate_reference_v2.yaml`
- Drafting + refinement use `llm_helpers.py` + prompt YAMLs
- Prompt refactor for `section_synthesizer` + `section_refiner`

Let me know when you’re ready to proceed with implementation 🚀