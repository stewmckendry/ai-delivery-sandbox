## 📋 Feature 5 – Task List: Dashboard + Data Export

### 📁 Planning
- [x] Create task in `feature_scope_tracker.md`
- [x] Draft and commit `plan.md`
- [x] Draft and commit `task_list.md`

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
- [ ] Add fields: `reporter_type`, `incident_context`, `sport_type`, `age_group`, `team_id`
- [ ] Update DB schema, models, and export tool to include metadata

### 🧪 Test
- [ ] Export test with known tracker/log pair
- [ ] DB validation (e.g., row counts, schema match)
- [ ] Power BI read test (real dashboard preferred)

### ✅ Wrap
- [ ] Confirm scope delivery
- [ ] Commit output sample + BI config
- [ ] Log reasoning trace and notes
- [ ] Notify Human Lead for review