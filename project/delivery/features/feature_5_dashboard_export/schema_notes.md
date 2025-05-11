## 🧾 Schema Notes – Feature 5: Data Export for Dashboard

### 📦 Tables

#### `tracker_export`
Used for reporting user recovery stage and triage info.

| Column        | Type     | Description                                |
|---------------|----------|--------------------------------------------|
| user_id       | string   | Unique user ID                             |
| current_stage | string   | Stage as inferred from symptom logs       |
| last_updated  | datetime | Timestamp from tracker state              |
| triage_level  | string   | Derived from triage YAML (e.g., red flag) |

#### `symptom_log_export`
Time-series symptom data for trend tracking.

| Column      | Type     | Description                                |
|-------------|----------|--------------------------------------------|
| user_id     | string   | Unique user ID                             |
| symptom_id  | string   | Symptom key from YAML                      |
| severity    | int      | 0–6 scale                                  |
| timestamp   | datetime | When symptom was logged                    |

---

### 🧩 YAML Influence
- `triage_map.yaml` determines triage level lookup per symptom
- `stages.yaml` is used to align logs to stage names if needed

---

### 🔄 Sync Strategy
- We batch export via `export_to_sql.py`
- Write logic uses SQLAlchemy `text()` for clarity
- Fields are extracted from existing tracker state and DB logs

---

### 🧠 Additional Metadata for Richer Dashboards

| Field            | Usefulness for Leaders                                   | Privacy Risk    | Changes Required                        |
|------------------|-----------------------------------------------------------|------------------|------------------------------------------|
| age_group        | Enables demographic breakdown of recovery timelines       | Medium           | Add age to user profile schema + export |
| sport_type       | Compare incidents across sports (e.g., football vs. soccer) | Medium           | Add to user/session metadata            |
| team_id          | Allows cohort comparisons by team/program                 | High             | Add mapping logic, consider de-ID       |
| incident_context | Analyze when/where injuries occur (e.g., practice vs. game)| High             | Extend symptom logger or new field      |
| reporter_type    | Distinguish self vs. coach reporting                      | Low              | Add to log_symptoms tool and DB schema  |

To support these, update `TrackerMetadata` or `SymptomLog` model, adjust YAML or UI flows to capture data, and extend `export_to_sql.py`.

---

All values are prepared for SQL insert and analytics.