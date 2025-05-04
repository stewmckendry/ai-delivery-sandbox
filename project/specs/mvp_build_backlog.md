## 🧱 MVP Build Backlog: AI CareerCoach

### 🔹 A. FastAPI Routes
- [x] `/load_prompt` – Load a coaching prompt by ID
- [x] `/get_yaml_segment` – Fetch career segment by category
- [ ] `/save_reflection` – Store a journaling reflection (Airtable/Notion)
- [ ] `/fetch_summary` – Retrieve all reflections for a session

### 🔹 B. Utilities
- [x] `prompt_loader.py` – Load JSON coaching prompts
- [x] `yaml_loader.py` – Fetch and parse YAML segments from GitHub
- [ ] `memory_manager.py` – Save/fetch reflections via Airtable and Notion
- [ ] `airtable_client.py` – Airtable integration
- [ ] `notion_client.py` – Notion integration

### 🔹 C. Schemas & Validation
- [ ] `prompt.py` – Define structure for coaching prompts
- [ ] `segment.py` – Define schema for career YAML segments
- [ ] `reflection.py` – Define input model for saving reflections

### 🔹 D. OpenAPI + GPT Interface
- [ ] Ensure `openapi.yaml` matches endpoints and GPT tools spec
- [ ] Tool contract: `/load_prompt`, `/get_yaml_segment`, `/save_reflection`, `/fetch_summary`

### 🔹 E. Testing & Logging
- [x] Unit tests for each route (use `pytest`, `httpx`)
- [ ] Mock Airtable and Notion clients
- [ ] Logging for tool failures and edge cases

### 🔹 F. Deployment Readiness
- [ ] `.env.template` with placeholders for tokens
- [ ] CI checks for linting + test pass
- [ ] Confirm Railway deployable via push to `main`