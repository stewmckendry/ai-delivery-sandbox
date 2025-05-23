# ✅ WP17b Task List – Section Draft Generation

## 📅 Status Tracker

### ✅ Planner & Toolchain
- [ ] Extend planner toolchain: `generate_section → compose_and_cite`
- [ ] Add `compose_and_cite` toolchain definition
- [ ] Register tools in tool_registry

### 🧠 Tool Creation
- [ ] Implement `memory_retrieve`
- [ ] Implement `section_synthesizer` (OpenAI Chat API)
- [ ] Implement `section_refiner` (OpenAI Chat API)

### 🗄️ Models + DB
- [ ] Create `ArtifactSection` model + SQL table
- [ ] Create `ReasoningTrace` model + SQL table
- [ ] Add save logic for both

### 🔍 Log + Trace
- [ ] `log_tool_usage` in each tool
- [ ] Implement PromptLog filter for input logs

### 🧪 Testing
- [ ] Create CLI to invoke pipeline (using sample input logs)
- [ ] Validate DB writes to `ArtifactSection`, `ReasoningTrace`
- [ ] Verify logs in PromptLog

### 🧾 Coordination
- [x] Submit plan to Human Lead ✅
- [ ] Provide midpoint update to Pod Lead
- [ ] Tag `queryCorpus` and embedding search as spillover

---

_Last updated: Revisions after HL feedback_