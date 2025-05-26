## 📋 WP22 Task List – GoC Alignment Search Tool

### 1. 🏗 Scaffolding
- [ ] Create empty files: `goc_alignment_search.py`, `queryCorpus.py`, `goc_alignment.py`, `goc_alignment_prompts.yaml`
- [ ] Register tool in `tool_catalog.yaml`, `gpt_tools_manifest.json`

### 2. 🧠 Implement Logic
- [ ] `queryCorpus.py`: Search pre-embedded corpus via Chroma
- [ ] `goc_alignment.py`: Restricted GoC web search with formatter + logger reuse
- [ ] `goc_alignment_prompts.yaml`: Templates for extracting alignment summaries

### 3. 🔁 Integration
- [ ] `goc_alignment_search.py`: Route to corpus or web based on availability
- [ ] Update `generate_section_chain.py` to optionally call alignment step
- [ ] Include result in inputs to `section_synthesizer`

### 4. 🧪 Testing
- [ ] `test_goc_alignment_tool.py`: CLI test toolchain execution and schema output

### 5. 📎 Documentation
- [ ] `WP22_toolchain_integration_note.md`: Developer reference for toolchain config

---

### 🧩 Notes
- Log alignment outputs in PromptLog + ReasoningTrace
- Leverage existing formatter + logging utilities from WP14
- Default to list-style citation output, support inline formatting if needed

---

### 🔍 Inputs Needed
- GoC corpus examples (actively being sourced)
- Web search scoped to *.gc.ca and other official GoC domains