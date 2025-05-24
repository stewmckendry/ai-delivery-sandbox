### 📋 WP18 Task List

#### 1. **Tool Development**
- [ ] `loadSectionMetadata.py` – Fetch + sort by `artifact_id`, `gate_id`
- [ ] `formatSection.py` – Apply Jinja/Markdown templates
- [ ] `mergeSections.py` – Merge formatted blocks
- [ ] `finalizeDocument.py` – Add TOC, header, layout
- [ ] `commitArtifact.py` – Save document, log to DB

#### 2. **Toolchain Registration**
- [ ] Define `assemble_artifact` chain in `planner_orchestrator.py`

#### 3. **Schemas + Validation**
- [ ] Pydantic schemas for tool inputs/outputs
- [ ] Validation logic in all tools

#### 4. **Logging**
- [ ] Integrate `log_tool_usage()` in all tools

#### 5. **Testing**
- [ ] CLI + API tests for each tool
- [ ] End-to-end toolchain test on Railway
- [ ] Use test data from `project/test/WP17b/`

#### 6. **Documentation**
- [ ] `WP18_template_reference.md`
- [ ] `WP18_gate_rendering_map.md`
- [ ] Implementation guide: GPT-safe fetch
- [ ] Drive integration spec for WP20