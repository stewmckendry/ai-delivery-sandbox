# ✅ WP17b Task List – Section Draft Generation

## 📅 Status Tracker

### Core Pipeline
- [ ] Extend planner toolchain: `generate_section → compose_and_cite`
- [ ] Implement `memory_retrieve` tool
- [ ] Implement `section_synthesizer` tool
- [ ] Implement `section_refiner` tool
- [ ] Add `ArtifactSection` write logic

### Traceability + Logging
- [ ] Ensure `log_tool_usage` is invoked for each step
- [ ] Save session snapshot + reasoning trace (YAML format)

### Testing
- [ ] Create CLI to trigger pipeline from inputs
- [ ] Create minimal test set with PromptLogs and memory entries
- [ ] Validate database writes for `ArtifactSection`

### Coordination
- [x] Submit design plan for Human Lead review
- [ ] Confirm assumptions (embedding availability, model schema)
- [ ] Request mid-point review with Lead Pod

---

Last updated: _initial commit_