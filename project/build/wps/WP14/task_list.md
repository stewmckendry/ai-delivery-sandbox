## WP14 Task List

### 📦 Tool Implementation
- [ ] `T1` - Implement `web_search.py` with routing logic
- [ ] `T2` - Build handlers for: `general`, `jurisdiction`, `market`
- [ ] `T3` - Write `web_search_formatter.py` for output normalization
- [ ] `T4` - Develop `web_search_logger.py` and `WebSearchLog` model
- [ ] `T5` - Create `search_prompts.yaml` with prompt variants

### 🔌 Integration
- [ ] `T6` - Register tool in `tool_catalog.yaml`
- [ ] `T7` - Add planner path in `planner_orchestrator.py`
- [ ] `T8` - Wire into `generate_section_chain.py` post-KB search

### 🧪 Testing & Docs
- [ ] `T9` - Toolchain integration test: fallback + formatting
- [ ] `T10` - Generate `WP14_toolchain_integration_note.md`
- [ ] `T11` - Write `WP14_search_tool_flow.md`
- [ ] `T12` - Document examples in `WP14_example_queries.md`