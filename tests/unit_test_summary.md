## 🧪 Unit Test Summary – CareerCoach MVP

### ✅ Scope of Coverage
This document summarizes the purpose and results of unit tests written to validate the CareerCoach MVP backend.

### 🔍 Targeted Modules and Endpoints

| Component | Type | Route or Function | Description | Linked Journey |
|----------|------|--------------------|-------------|-----------------|
| prompt_loader.py | Utility | `load_prompt(prompt_id)` | Loads structured JSON prompt | 👧 Explorer → Prompt selector
| yaml_loader.py | Utility | `load_segment(category)` | Loads a YAML segment from repo | 👧 Explorer → Career card
| memory_manager.py | Utility | `save_to_memory()` | Persists journaling reflections | 👧 Explorer → Journaling
| /load_prompt | Route | GET | Fetches prompt by ID | 👧 Explorer
| /get_yaml_segment | Route | GET | Loads career YAML by category | 👧 Explorer
| /record_reflection | Route | POST | Saves a reflection object | 👧 Explorer

### 🧠 Contextual Integration
- These routes and tools map directly to the Explorer journey and stack described in `stack_and_component_design.md`
- Prompts guide journaling → Segment supports career suggestions → Reflection saves complete the feedback loop

### ✅ Results (as expected)
| Test | Status | Notes |
|------|--------|-------|
| `test_load_prompt` | ✅ Pass / 404 (OK) | Endpoint responds with prompt or error |
| `test_get_yaml_segment` | ✅ Pass / 404 (OK) | Endpoint resolves or handles missing YAML |
| `test_record_reflection` | ✅ Pass | Returns 200 if text is valid |
| `test_prompt_loader` | ✅ Pass / fallback | Handles valid & error conditions |
| `test_yaml_loader` | ✅ Pass / fallback | Confirms segment format & catch errors |

---

### 🧭 Next Steps
- CI integration with GitHub Actions
- Expand tests for error conditions (e.g. bad payloads, invalid keys)
- Add test for session_id summarization in memory_manager
- Handoff coverage matrix to QAPod