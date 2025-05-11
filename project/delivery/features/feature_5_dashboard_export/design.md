## 🧠 Feature 5 – Design: Azure Dashboard + Data Export

### 📊 Export Schema
We'll export to two primary tables:

#### `tracker_export`
| Field         | Type     | Source                        |
|---------------|----------|-------------------------------|
| user_id       | string   | `tracker_state['user_id']`    |
| current_stage | string   | `tracker_state['state']['stage']` |
| last_updated  | datetime | `tracker_state['updated_at']` |
| triage_level  | string   | inferred from triage YAML     |

#### `symptom_log_export`
| Field        | Type     | Source                  |
|--------------|----------|-------------------------|
| user_id      | string   | `symptom_log.user_id`   |
| symptom_id   | string   | `symptom_log.symptom_id`|
| severity     | int      | `symptom_log.severity`  |
| timestamp    | datetime | `symptom_log.timestamp` |

---

### 🔗 YAML Mappings

- Use `triage_map.yaml` to associate symptoms with triage levels.
- Use `stages.yaml` to classify logs by recovery phase.
- Each log row will be augmented with YAML-derived fields during export.

---

### 📁 File Outputs
- `app/tools/export_to_sql.py`: main export logic
- `project/delivery/features/feature_5_dashboard_export/schema_notes.md`
- `project/delivery/features/feature_5_dashboard_export/dashboard_flow.md`

---

### 📊 Power BI Targets

#### Audience
- Sports system leaders responsible for concussion protocols, return-to-play policy, and league-wide health trends

#### Views
- Symptom frequency by time
- Stage duration per user
- Return-to-play readiness
- Aggregate incident rates by team, age, gender, or sport (if metadata is added)

#### Data Sources
- Azure SQL (read access)

---

Let me know if you'd like to preview the Power BI dashboard or prioritize any field or chart.