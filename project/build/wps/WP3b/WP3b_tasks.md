## WP3b Task Tracker – Tool Wrapping + API

### ✅ Planning & Design
- [x] Review WP3b_definition.md and supporting files
- [x] Draft and commit WP3b_design.md

### 🚧 Build Stages

#### T1: Registry + Config
- [ ] Scaffold `tool_registry.py`
- [ ] Create `project/reference/tool_catalog.yaml`
- [ ] Create `project/reference/integrations.yaml`

#### T2: Tool Wrappers
- [ ] Stub 1-2 example tools per `tool_catalog_v2.md`
- [ ] Implement `run_tool(input_dict)` and CLI fallback

#### T3: API Routing
- [ ] Scaffold `api_router.py`
- [ ] Wire router to registry
- [ ] Create `/tools/{tool_id}` route + `/status`

#### T4: OpenAPI Schema
- [ ] Auto-generate initial OpenAPI schema from FastAPI
- [ ] Patch overrides where needed (matching `api_contracts_v2.md`)

#### T5: Docs + Examples
- [ ] Draft `WP3b_openapi_coverage.md`
- [ ] Draft `WP3b_registration_examples.md`

#### T6: Test + Deploy
- [ ] Create `main.py` with test server
- [ ] Add Railway deploy script and instructions
- [ ] Validate all endpoints + schema

### 🔁 Feedback & Wrap
- [ ] Share build and request HL review
- [ ] Fix issues from test or review
- [ ] Final update to Lead Pod with file links