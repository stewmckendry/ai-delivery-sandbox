## 🧭 Feature 5 – Azure Dashboard + Data Export

### 🎯 Goal
Enable clinical and operational analytics by exporting tracker and symptom log data to an Azure SQL-backed dashboard (Power BI compatible). Support trend analysis, return-to-play decisions, and population-level insights.

### ✅ In Scope
- Write periodic exports of `TrackerState` and `SymptomLog` to Azure SQL
- Prototype Power BI dashboard: timelines, flags, trends
- Include YAML stage definitions and triage mappings in export
- Add metadata: user stage, symptom severity, timestamp, triage level
- Add test coverage for export format and scheduling

### 🚫 Out of Scope
- Real-time sync engine (will prototype batch dump)
- Full production dashboard UX (Power BI only)

### 📥 Inputs
- TrackerState JSON (`app/models/tracker.py`)
- Symptom logs from DB (`SymptomLog`)
- Stages YAML (`reference/stages.yaml`)
- Triage map YAML (`reference/triage_map.yaml`)

### 📤 Outputs
- `export_to_sql.py` tool
- Updated DB schema if needed
- Sample exported tables
- Power BI config + screenshot(s)

### 🔗 Dependencies
- Feature 2 tracker + log schema
- Feature 1 triage map + levels
- Azure SQL database access

---

Next: task list and deliverables breakdown