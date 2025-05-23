# ✅ WP17b Task List – Section Draft Generation

## 📅 Status Tracker

### ✅ Planner & Toolchain
- [x] Extend planner toolchain: `generate_section → GenerateSectionChain`
- [x] Add `GenerateSectionChain` class definition
- [x] Register tools in tool_registry + manifest

### 🧠 Tool Creation
- [x] Implement `memory_retrieve`
- [x] Implement `section_synthesizer` (OpenAI Chat API)
- [x] Implement `section_refiner` (OpenAI Chat API)

### 🗄️ Models + DB
- [x] Create `ArtifactSection` model + SQL table
- [x] Create `ReasoningTrace` model + SQL table
- [ ] Add save logic for both

### 🔍 Log + Trace
- [ ] `log_tool_usage` in each tool
- [x] Implement PromptLog filter for input logs

### 🧪 Testing
- [x] Create CLI to invoke pipeline (using sample input logs)
- [x] Validate toolchain end-to-end execution
- [ ] Validate DB writes to `ArtifactSection`, `ReasoningTrace`
- [ ] Verify logs in PromptLog

### 🧾 Coordination
- [x] Submit plan to Human Lead ✅
- [ ] Provide midpoint update to Pod Lead
- [ ] Tag `queryCorpus` and embedding search as spillover

---

_Last updated: Post test success_