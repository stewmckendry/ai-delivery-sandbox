## WP3b Design Plan – Tool Wrapping + API Layer

### 🎯 Outcomes (from WP3b_definition.md)
- Register all tools defined in `tool_catalog_v2.md`
- Expose tools as API endpoints via a unified router
- Define complete OpenAPI spec for all tool I/O
- Ensure configuration is centralized and testable
- Validate that all API endpoints are functioning

### 📦 Deliverables Traceability
| File | Purpose | Design Notes |
|------|---------|--------------|
| `app/tools/tool_registry.py` | Central dynamic loader | Uses `importlib`, loads from `tool_catalog.yaml` |
| `app/tools/tool_wrappers/*.py` | Tool wrappers | Normalize I/O per OpenAPI spec |
| `app/engines/api_router.py` | API endpoint setup | FastAPI routes using registry |
| `main.py` | Entry + server init | Loads config, registry, runs FastAPI app |
| `app/openapi/openapi_schema.yaml` | API spec | Generated from FastAPI with overrides |
| `project/reference/tool_catalog.yaml` | Tool metadata | CLI + API registration, paths, keys |
| `project/reference/integrations.yaml` | Service config | Auth + external URLs |
| `WP3b_openapi_coverage.md` | Coverage matrix | Traces tool → schema |
| `WP3b_registration_examples.md` | Code snippets | Show wrapper and FastAPI endpoint |

### 📐 Assumptions
- Tools will use FastAPI for wrapping and exposure
- Railway cloud will be used for hosting (FastAPI + Uvicorn)
- Tools emit structured YAML blocks for traceability
- CLI testing precedes API integration for faster iteration

### 🏗️ Implementation Plan

#### T1: `tool_registry.py`
- Load from `tool_catalog.yaml`
- Validate presence of `run_tool(input: dict) -> dict`
- Support tagging and categorization for API groups

#### T2: Wrappers
- For each tool in `tool_catalog_v2.md`
  - Stub or wrap with `run_tool(input_dict)`
  - Add CLI fallback: `python tool.py --input input.yaml`
  - Emit YAML blocks: input, output, error

#### T3: `api_router.py`
- Generate routes from registry
- Route path: `/tools/{tool_id}`
- Accept and return JSON
- Add healthcheck `/status`

#### T4: OpenAPI Schema
- Use FastAPI autogen, override manually where needed
- Ensure parameters match spec in `api_contracts_v2.md`
- Versioned endpoint group `/v1/`

#### T5: Config Files
- `tool_catalog.yaml`: entry path, name, input schema ref
- `integrations.yaml`: any service URLs, keys, timeouts

#### T6: Docs + Examples
- `WP3b_openapi_coverage.md`: trace each route to tool
- `WP3b_registration_examples.md`: CLI + API examples

#### T7: Deployment Plan
- Local test using Uvicorn (`main.py`)
- Railway deploy script: `railway.json` + README

### ✅ Acceptance Criteria Mapping
| Criteria | Design Approach |
|----------|-----------------|
| All tools registered | Registry and config-driven loader |
| API router functional | FastAPI dynamic route creation |
| OpenAPI schema valid | Spec generation with manual checks |
| Centralized config | `tool_catalog.yaml`, CLI + API |
| Testable endpoints | Stub + YAML emit per tool + test route |

### 🧪 Build Guidance (from prior WPs)
- **CLI-first** for fast iteration
- **Trace YAML** with hashes for test logs
- **Stub early** to validate paths
- **Validate fields** early (e.g., `gate_id`, `section_id`)
- **Log everything**: I/O, errors in YAML

### 🤝 Coordination Notes
- Link tool output to memory model (WP3a)
- Align output format with `api_contracts_v2.md`
- Log inputs/outputs for WP4 traceability

---

Ready to begin scaffolding and stubbing once this is approved. Next up: task tracker + initial file stubs.