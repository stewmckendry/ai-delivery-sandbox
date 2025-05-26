# WP22 Definition – GoC Alignment Search Tool

## 🧠 Summary
Design and implement a tool that retrieves Government of Canada priorities and strategies relevant to the current artifact section, helping demonstrate alignment for stronger approvals.

## 🎯 Objective
Build a `goc_alignment_search` tool to:
- Search or query known government content (static or web)
- Return structured summary and references
- Integrate with the `generate_section_chain` toolchain

---

## 🧱 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/tools/tool_wrappers/goc_alignment_search.py` | Entry point for planner and GPT |
| `app/tools/tool_wrappers/queryCorpus.py` | Queries embedded documents loaded by `loadCorpus` |
| `project/prompts/goc_alignment_prompts.yaml` | Prompt templates for summarization |
| `project/build/WPs/WP22/WP22_toolchain_integration_note.md` | Registration guide and planner flow |

---

## 📘 Supporting Docs
| File Path | Description |
|-----------|-------------|
| `WP22_design_note.md` | Tool purpose, strategies, and plan |
| `tool_catalog.yaml`, `gpt_tools_manifest.json` | Tool registration entries |

---

## 🔁 Toolchain Integration
- Optional step in `generate_section_chain`
- Outputs included as `alignment_support` in `section_synthesizer`
- Logs results in PromptLog and ReasoningTrace

---

## 🧪 Testing
| File Path | Description |
|-----------|-------------|
| `test_goc_alignment_tool.py` | CLI validation of results, logs, output schema |

---

## 🧠 Lessons Learned to Apply
- Model tools for traceability and reproducibility
- Build modular steps that can be rerun or debugged
- Validate schema at tool boundary

---

## 📎 Related WPs
- WP14 (external search)
- WP17b (toolchains, ReasoningTrace)
- WP7 (project profile context)

## 🔮 Future Extensions
- Annotate alignment with confidence levels
- Link alignment to Gate schema fields
- Support per-section or per-project scanning