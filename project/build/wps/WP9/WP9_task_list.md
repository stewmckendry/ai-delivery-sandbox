### ✅ WP9 Task List – Input Ingestion System

#### 🔧 Dev Owner: WP9Pod
#### 📂 Repo: `ai-delivery-sandbox`, Branch: `sandbox-curious-falcon`

---

### 🧱 Phase 1 – Setup + Scaffolding
- [ ] T1: Create `text_extractor.py` – parse .pdf/.docx/.txt
- [ ] T2: Create `structured_input_ingestor.py` – structure & tag content
- [ ] T3: Create `retry_ingestion.py` – retry logic
- [ ] T4: Stub CLI script to invoke tool wrappers

---

### ⚙️ Phase 2 – Tool Wrappers
- [ ] T5: Implement `uploadTextInput` tool wrapper
- [ ] T6: Implement `uploadFileInput` tool wrapper
- [ ] T7: Implement `uploadLinkInput` tool wrapper
- [ ] T8: Validate with `tool_registry.py` and schema

---

### 🧪 Phase 3 – Logging + Test Harness
- [ ] T9: Integrate with `memory_sync.py` – log YAML traces
- [ ] T10: Emit `PromptLog` + `SessionSnapshot`
- [ ] T11: Generate YAML ingestion trace format
- [ ] T12: Write CLI test plan using sample inputs

---

### 📦 Phase 4 – Registry Integration
- [ ] T13: Add tools to `tool_catalog.yaml`
- [ ] T14: Create schema for input ingestion tools
- [ ] T15: Add entries to `gpt_tools_manifest.json`

---

### 🧾 Phase 5 – Final Wrap + Docs
- [ ] T16: Document ingestion flow (`WP9_input_summary_flow.md`)
- [ ] T17: Retrospective + status update

---

### 🚀 Ready for Execution
URL: [WP9_task_list.md](https://github.com/stewmckendry/ai-delivery-sandbox/blob/sandbox-curious-falcon/project/build/wps/WP9/WP9_task_list.md)