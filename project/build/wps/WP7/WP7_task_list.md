## WP7 Task List

### ✅ Infra & DB
- [x] Define `ProjectProfile` table schema
- [ ] Implement Alembic migration
- [ ] Add SQLAlchemy model
- [ ] Add `project_id` FK to all major tables (ArtifactSection, ReasoningTrace, etc.)
- [ ] Create `project_profile_schema.py` model
- [ ] Generate SQL CREATE TABLE for `ProjectProfile`

### 📊 Core Engine
- [ ] `project_profile_engine.py` with:
  - [ ] `save_profile(dict)`
  - [ ] `load_profile(project_id)`
  - [ ] `validate_profile(dict)`

### 🔹 Toolchain Patches
- [ ] `generate_section_chain.py` – inject profile into memory
- [ ] `assemble_artifact_chain.py` – include profile in finalization
- [ ] `planner_orchestrator.py` – load profile at start
- [ ] `memory_sync.py` – add profile save/load
- [ ] New `IngestInputChain.run()` – profile init from uploaded input (wired to `uploadTextInput`, `uploadFileInput`, `uploadLinkInput`)
- [ ] Add tool for human profile confirmation + edit (Canvas / GPT prompt support)

### 📂 Drive Integration
- [ ] Update `storeToDrive.py` to include `project_id`

### 📄 Documentation
- [ ] YAML schema: `reference/project_profile_schema.yaml`
- [ ] Usage doc: `build/wps/WP7/project_profile_usage_notes.md`