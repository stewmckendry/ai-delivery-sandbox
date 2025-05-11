## 📋 Feature 5 – Task List: Dashboard + Data Export

### 📁 Planning
- [x] Create task in `feature_scope_tracker.md`
- [x] Draft and commit `plan.md`
- [x] Draft and commit `task_list.md`
- [ ] Document and validate tool catalog (triage, assessment, export)

### 📐 Design
- [x] Define export schema: which fields go where
- [x] YAML and tracker field mapping docs
- [x] Sample Power BI config (mock or real)
- [x] Document metadata enrichment opportunities

### 🛠 Build
- [x] Tool: `export_to_sql.py`
- [x] YAML + Tracker field extractors (`reference_loader.py`)
- [x] SQL insert/update logic
- [ ] Scheduled or manual export mode
- [x] Document export process + frequency in addendum
- [x] Add fields: `reporter_type`, `incident_context`, `sport_type`, `age_group`, `team_id`
- [x] Update DB schema, models, and export tool to include metadata
- [x] Update `symptoms.py` to add metadata to `SymptomCheckIn`
- [x] Update `db_writer.py` to persist new metadata fields
- [x] Update `export_to_sql.py` to export metadata fields
- [x] Update `clinical_summary.html` to show metadata
- [x] Update `epic_writer.py` to include metadata as Observation notes
- [x] Update `pdf_renderer.py` to render new metadata fields
- [x] Add triage questions for `sport_type`, `age_group`, `team_id`
- [x] Update `triage_map.yaml` to include new metadata questions
- [x] Update triage test flows to cover new question types (if affected)
- [x] Map triage question responses from `TrackerState.answers` into symptom metadata
- [ ] Confirm GPT orchestration persists triage answers to `TrackerState` (e.g., via `assess_concussion`)
- [ ] Build tools to support triage orchestration: `get_triage_flow`, `get_triage_question`, `assess_concussion`, `log_incident_detail`

### 🧪 Test
- [ ] Export test with known tracker/log pair
- [ ] DB validation (e.g., row counts, schema match)
- [ ] Power BI read test (real dashboard preferred)

### ✅ Wrap
- [ ] Confirm scope delivery
- [ ] Commit output sample + BI config
- [ ] Log reasoning trace and notes
- [ ] Notify Human Lead for review