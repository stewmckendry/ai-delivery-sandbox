## ✅ CareerCoach MVP Deployment Checklist

### 🔧 System Setup
- [x] FastAPI app with route modules
- [x] `main.py` with unified routers
- [x] `.env.template` ready
- [x] Railway GitHub integration done
- [x] Railway start command configured

### 🧪 Testing & Validation
- [x] Manual endpoint testing
- [ ] ⬜ Unit test coverage for FastAPI routes
- [ ] ⬜ Unit test coverage for utils (prompt_loader, yaml_loader, memory_manager)
- [ ] ⬜ Pre-deploy validation script (import/env check)

### 📚 Prompt System
- [x] 10 schema-valid prompts in JSON
- [ ] ⬜ Split prompts into per-ID files
- [ ] ⬜ Wire prompt selector UI in GPT tool

### 🔌 Integrations
- [x] Airtable + Notion tokens and base IDs tested
- [x] Railway secrets configured

### 🔁 CI/CD
- [ ] ⬜ Add GitHub Action for lint/test/deploy
- [x] Manual Railway deployment works

### 🧠 GPT Integration
- [x] Custom GPT `CareerCoach-GPT` scaffolded with OpenAPI tools
- [x] Tools: `/load_prompt`, `/get_yaml_segment`, `/save_reflection`, `/fetch_summary` declared
- [ ] ⬜ Validate tools wire correctly to FastAPI endpoints
- [ ] ⬜ Confirm fallback UX (invalid prompt_id, network errors, empty state)

### 🧑‍🏫 Frontend Use Cases
- [ ] ⬜ Prompt Selector UI pulls from committed prompt IDs
- [ ] ⬜ Guided Q&A mode uses loaded prompt content
- [ ] ⬜ Career Card UX validates YAML segment loading and formatting
- [ ] ⬜ Journaling flow saves and summarizes reflections correctly
- [ ] ⬜ Session continuity via session_id maintained

### 🧠 Handoff Prep
- [ ] ⬜ Final test script or curl examples for QAPod
- [ ] ⬜ Prompt test coverage confirmed
- [ ] ⬜ Prepare QA onboarding brief with flows and tool mappings