# WP25 Definition – GPT Tool Discoverability & Description

## 🧠 Summary
Enable GPT to better understand what tools are available, what they do, how to use them, and when to call them during document workflows.

## 🌟 Objective
Improve and operationalize GPT access to system tool documentation by:
- Expanding `gpt_tools_manifest.json` with schemas, I/O types, and call contexts
- Creating a browsable `tool_catalog.yaml` with GPT-readable summaries
- Developing a lightweight indexing tool (`tool_registry_builder`) to sync both sources

---

## 🧱 Deliverables
| File Path | Description |
|-----------|-------------|
| `project/reference/tool_catalog.yaml` | Rich tool descriptions for GPT lookup |
| `project/reference/gpt_tools_manifest.json` | Updated JSON manifest with enhanced fields |
| `app/tools/tool_utils/tool_registry_builder.py` | Builds and validates index from code + prompts |
| `project/build/wps/WP25/WP25_metadata_plan.md` | Field model and examples |

---

## 🔁 Integration
- Referenced by GPT in tool planning, search, and selection flows
- Used in bootstrapping new GPT pods and for reindexing tools

---

## 🧪 Testing
| File Path | Description |
|-----------|-------------|
| `project/test/wps/WP25/test_tool_registry_builder.py` | Validates JSON+YAML integrity and link resolution |

---

## 🔮 Future Extensions
- GPT agent memory to cache and suggest commonly used tools
- Endpoint for querying tool metadata at runtime: `/tools/query_available_tools`
- Support for tagging tools with SDLC phase, persona, input style, and PoD ownership