## WP14 Task List

### 📦 Tool Implementation
- [x] `T1` - Implement `web_search.py` with routing logic
- [x] `T2` - Build handlers for: `general`, `jurisdiction`, `market`
- [x] `T3` - Write `web_search_formatter.py` for output normalization
- [x] `T4` - Develop `web_search_logger.py` and `WebSearchLog` model
- [x] `T5` - Create `search_prompts.yaml` with prompt variants

### 🔌 Integration
- [x] `T6` - Register tool in `tool_catalog.yaml`
- [ ] `T7` - Add planner path in `planner_orchestrator.py`
- [ ] `T8` - Wire into `generate_section_chain.py` post-KB search

### 🧪 Testing & Docs
- [ ] `T9` - Toolchain integration test: fallback + formatting
- [ ] `T10` - Generate `WP14_toolchain_integration_note.md`
- [ ] `T11` - Write `WP14_search_tool_flow.md`
- [x] `T12` - Document examples in `WP14_example_queries.md`

### 🔍 Search Integration
- [ ] `T13` - Implement real API search in `general.py`
- [ ] `T14` - Enhance `jurisdiction.py` with domain filters or query parsing
- [ ] `T15` - Enhance `market.py` with vertical search sources or APIs