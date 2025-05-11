## 🔄 Data Flow Addendum – Metadata from Triage to Dashboard

This addendum describes the end-to-end flow of metadata (e.g., reporter type, sport, age group) from triage collection through symptom logging, database storage, and export to Power BI.

---

### 📥 Step 1: Collection in Triage Flow
- **Source**: `triage_map.yaml`
- **Tool**: `triage_engine.py`
- **Storage**: `TrackerState.answers`
- **Fields Collected**:
  - `reporter_type` → e.g., self, coach
  - `incident_context` → e.g., game, practice
  - Proposed: `sport_type`, `age_group`, `team_id`

### 📤 Step 2: Logging via Symptom Tool
- **Input**: `SymptomCheckIn` (in `symptoms.py`)
- **Tool**: `symptom_logger.py`
- **Mapping**: TrackerState.answers → `payload.metadata`
- **Storage**: `log_symptoms_to_db()` writes to SQLAlchemy `SymptomLog`
- **Fields Persisted**:
  - `reporter_type`, `incident_context`, `sport_type`, `age_group`, `team_id`

### 🛢 Step 3: Database Layer
- **Model**: `SymptomLog` (in `db_models.py`)
- **Schema**: Adds new metadata columns with appropriate types

### 📊 Step 4: Export to Azure SQL
- **Tool**: `export_to_sql.py`
- **YAML Reference**: `reference_loader.py` (triage/stage enrichment)
- **Tables**: `tracker_export`, `symptom_log_export`
- **Metadata Included** in `symptom_log_export`

### 📈 Step 5: Power BI Dashboard
- **Source**: Azure SQL (via read access)
- **View**: `dashboard_flow.md`
- **Fields Used For**:
  - Group filters by team, age group, sport
  - Trendline segmentation by context or reporter type

---

### 🔁 Recap: File Responsibilities
| Step | File/Module | Role |
|------|-------------|------|
| 1    | triage_map.yaml | Define questions and options |
| 2    | triage_engine.py | Store answers to `TrackerState` |
| 3    | symptom_logger.py | Map and log metadata |
| 4    | db_writer.py | Persist metadata to DB |
| 5    | db_models.py | Schema definition |
| 6    | export_to_sql.py | Export to SQL |
| 7    | dashboard_flow.md | Document dashboard use case |

This provides traceability and clarity for every step in the metadata capture pipeline.