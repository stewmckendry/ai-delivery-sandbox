## 🧪 Unit Test Summary – CareerCoach MVP

### ✅ Scope of Coverage
This document summarizes the purpose and results of unit and tool tests validating the CareerCoach MVP backend.

### 🔍 Targeted Modules and Endpoints

| Component | Type | Route or Function | Description | Linked Journey |
|----------|------|--------------------|-------------|-----------------|
| prompt_loader.py | Utility | `load_prompt(prompt_id)` | Loads structured JSON prompt | 👧 Explorer → Prompt selector
| yaml_loader.py | Utility | `load_segment(category)` | Loads a YAML segment from repo | 👧 Explorer → Career card
| memory_manager.py | Utility | `save_to_memory()` | Persists journaling reflections | 👧 Explorer → Journaling
| airtable_client.py | Client | `save_to_airtable`, `get_reflection` | Reflection persistence and retrieval | 👧 Explorer → Reflection
| notion_client.py | Client | `save_to_notion` | Logs prompt and reflection data | 👧 Explorer → Journaling log
| /load_prompt | Route | GET | Fetches prompt by ID | 👧 Explorer
| /get_yaml_segment | Route | GET | Loads career YAML by category | 👧 Explorer
| /record_reflection | Route | POST | Saves a reflection object | 👧 Explorer
| /fetch_summary | Route | GET | Retrieves latest reflection for summary | 👧 Explorer

### 🧠 Contextual Integration
- These routes and tools map directly to the Explorer journey and stack described in `stack_and_component_design.md`
- Prompts guide journaling → Segment supports career suggestions → Reflection saves complete the feedback loop

### ✅ Results (as expected)
| Test | Status | Notes |
|------|--------|-------|
| `test_load_prompt` | ✅ Pass / 404 (OK) | Endpoint responds with prompt or error |
| `test_get_yaml_segment` | ✅ Pass / 404 (OK) | Endpoint resolves or handles missing YAML |
| `test_record_reflection` | ✅ Pass | Saves to both Airtable and Notion |
| `test_fetch_summary` | ✅ Pass | Successfully retrieves saved reflection |
| `test_prompt_loader` | ✅ Pass / fallback | Handles valid & error conditions |
| `test_yaml_loader` | ✅ Pass / fallback | Confirms segment format & catch errors |

### 🐞 Bugs Discovered & Resolved
| Issue | Fix |
|-------|-----|
| Reflection not saving | Added missing POST route, fixed Notion schema & Airtable table config |
| Prompt content missing | Unpacked nested `content` field from prompt JSON |
| 403 / 401 / 422 Airtable errors | Replaced table name, adjusted token scopes, and fixed field types |
| fetch_summary failed | Added route + simplified to direct lookup |
| CreatedDate and PromptContent missing | Updated field names and formatted values for Notion |

### 📘 Lessons Learned
- Always verify Airtable and Notion schema names match backend field keys
- Use default ISO timestamp and slice when Notion expects `YYYY-MM-DD`
- Prompt JSON format changes (like `content`) must propagate to loaders & submitters

---

### 🧭 Next Steps
- CI integration with GitHub Actions
- Expand tests for error conditions (e.g. bad payloads, invalid keys)
- Add test for session_id summarization in memory_manager
- Handoff coverage matrix to QAPod