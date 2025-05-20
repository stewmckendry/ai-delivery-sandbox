## WP ID: WP3b
## WP Name: Tool Registration + API Wrapping

### 🌟 Outcome
By the end of this WP, the system will be able to expose registered tools via a unified API interface, enabling structured access, integration, and orchestration through GPT and external calls.

### 🧽 Scope
**In Scope:**
- Dynamic registration of tools
- Wrapping tools with standard interface
- API router setup
- Configuration via tool and integration files
- OpenAPI specification

**Out of Scope:**
- Planner execution or orchestration (WP3a)
- Tool call error handling (WP3c)

### 📦 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/tools/tool_registry.py` | Central registry where tools are declared and loaded. |
| `app/tools/tool_wrappers/*.py` | Standard wrappers to normalize tool interfaces. |
| `app/engines/api_router.py` | Unified router exposing tools via OpenAPI endpoints. |
| `main.py` | Entry point that registers tools and starts the API server. |
| `app/openapi/openapi_schema.yaml` | Full schema describing available tools, I/O formats. |
| `config/tool_config.yaml` | Tool-specific configuration (keys, metadata, flags). |
| `config/integrations.yaml` | Integration settings (external service endpoints, auth). |

### 📄 Supporting Documentation (to generate)
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WP3b/WP3b_openapi_coverage.md` | Table showing how each tool maps to OpenAPI schema. |
| `project/build/wps/WP3b/WP3b_registration_examples.md` | Code snippets for tool registration and test routes. |

### ✅ Acceptance Criteria
- [ ] All tools from `tool_catalog_v2.md` are implemented and registered
- [ ] API router exposes each tool with a working route
- [ ] OpenAPI schema validates and documents tool parameters
- [ ] Tool config is centralized and testable

### 🛠 Tasks
| Task ID | Description |
|---------|-------------|
| T1 | Implement `tool_registry.py` and dynamic loader |
| T2 | Implement standard wrappers for each tool |
| T3 | Implement `api_router.py` to expose endpoints |
| T4 | Define and validate `openapi_schema.yaml` |
| T5 | Configure tools in `tool_config.yaml` and `integrations.yaml` |
| T6 | Write test endpoints and confirm tool I/O flows |

### 📚 Reference Documentation
| File Path | Usage |
|-----------|--------|
| `tool_catalog_v2.md` | Source of tools to implement and register |
| `api_contracts_v2.md` | Reference for OpenAPI and parameter specs |
| `system_architecture_v2.md` | Overview of tool access and routing |
| `data_flow_master_v2.md` | API and tool invocation path |

### 📝 Notes to Development Team
- Use standardized wrapper signatures to ensure planner compatibility.
- Ensure API router includes versioning and health check routes.
- Follow OpenAPI 3.1 spec strictly to support SDK generation and testing.

---

All tools in `tool_catalog_v2.md` are covered in this WP. Each will:
- Have a corresponding wrapper
- Be registered in `tool_registry.py`
- Be exposed via the unified API router
- Be covered in the OpenAPI spec
- Be testable via route simulations