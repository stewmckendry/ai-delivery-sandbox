# WP25 Definition – GPT Tool Discoverability & Description

## 🧠 Summary
Enable GPT to better understand what tools are available, what they do, how to use them, and when to call them during document workflows.

## 🎯 Objective
Improve and operationalize GPT access to system tool documentation by:
- Expanding `gpt_tools_manifest.json` with schemas, I/O types, and call contexts
- Creating a browsable `tool_catalog.yaml` with GPT-readable summaries
- Developing a lightweight indexing tool (`tool_index_builder`) to sync both sources

---

## 🧱 Deliverables
| File Path | Description |
|-----------|-------------|
| `project/reference/tool_catalog.yaml` | Rich tool descriptions for GPT lookup |
| `project/reference/gpt_tools_manifest.json` | Updated JSON manifest with enhanced fields |
| `app/tools/tool_utils/tool_index_builder.py` | Tool to build and validate index from code + prompts |
| `project/build/wps/WP25/WP25_metadata_plan.md` | Field model and examples |

---

## 🔁 Integration
- Called by GPT when planning or selecting toolchain
- Referenced in prompt bootstraps or UI-based GPT instructions

---

## 🧪 Testing
| File Path | Description |
|-----------|-------------|
| `test_tool_index_builder.py` | Validates JSON+YAML structure + links to code |

---

## 🔮 Future Extensions
- GPT-agent memory to store frequently used tools
- Real-time query to discover latest tools via `/tools/query_available_tools` endpoint