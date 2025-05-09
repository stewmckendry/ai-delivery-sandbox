## 📊 Spike Report: Power BI Dashboard Design for Concussion Recovery GPT

---

### 🎯 Objective
Design the data structure, filters, and metrics to support system-level monitoring via Power BI. This enables sport administrators and health system actors to visualize concussion trends and recovery compliance.

---

### 🧭 Goals of the Dashboard
- Track total incidents, flagged risks, and stage progression
- Enable filtering by sport, age, gender, recovery stage, and timeframe
- Compare recovery patterns across cohorts
- Surface metrics on readiness for return-to-play

---

### 📌 Proposed Filters
| Filter              | Field in DB           | Notes                                     |
|---------------------|------------------------|--------------------------------------------|
| Date Range          | `incident_date`, `last_checkin` | Support monthly/quarterly trends          |
| Sport               | `sport`               | Captured at incident intake                |
| Age Group           | `age`                 | Bucketed into cohorts (U12, U16, etc.)     |
| Gender              | `gender`              | From incident intake or wearable profile   |
| Recovery Stage      | `current_stage`       | Derived from `stages.yaml` logic           |
| Incident Severity   | `risk_flag`           | From `flag_risk` tool output               |

---

### 📈 Key Metrics
| Metric                          | Source                            | Type        |
|----------------------------------|-----------------------------------|-------------|
| Total Incidents Logged          | Tracker DB                        | Count       |
| High Risk Flags Triggered       | `flag_risk` logs                  | Count       |
| Average Recovery Duration       | `incident_date` to `return_stage` | Duration    |
| Current Recovery Stage Spread   | Tracker DB                        | Histogram   |
| Daily/Weekly Check-In Compliance| Symptom DB                        | Ratio       |
| Ready for Return-to-Play        | `stage == cleared`               | Count       |

---

### 🗃️ Tracker vs. Symptom DB

The system uses two complementary databases:

- **Tracker DB**: Stores one record per concussion case (created at incident intake). Includes metadata like sport, age, gender, current stage, and risk flags. This serves as the athlete's "case file."
- **Symptom DB**: Logs daily check-ins (one row per day). Tracks symptoms over time, used to measure recovery compliance and stage inference. Think of this as a daily journal.

They are linked by `tracker_id` and used together for dashboard metrics and clinical summaries.

### 🗃️ Tracker Metadata Capture
During the initial incident intake via GPT, the following fields are captured and stored as part of the tracker:

- **Sport**: "What sport were they playing?"
- **Age**: "How old is the athlete?"
- **Gender**: "How do they identify (optional)?"

These are stored once and linked to the tracker record, ensuring availability for dashboards and exports.

### 🗃️ Backend Staging Schema (for Azure)
We'll export a denormalized flat table with one row per tracker:

```sql
CREATE TABLE concussion_dashboard_export (
  tracker_id TEXT,
  user_id TEXT,
  incident_date DATE,
  last_checkin DATE,
  sport TEXT,
  age INT,
  gender TEXT,
  current_stage TEXT,
  risk_flag BOOLEAN,
  total_symptom_logs INT,
  avg_symptom_severity FLOAT,
  recovered BOOLEAN,
  export_date DATE
);
```

- Exported via batch job from FastAPI
- Pulled into Power BI via Azure SQL connector

---

### 📉 Power BI Design Notes
- Use slicers for filter fields (sport, stage, etc.)
- Time-based visuals: bar charts for trends, line graphs for recovery time
- Use conditional formatting to highlight late recoveries or missing data
- Enable exporting filtered views (PDF, Excel)

---

### 📌 Open Questions
- Should we support multi-user tracker sharing (e.g., coaches linked to multiple players)?
- Should wearable stats be included (e.g., average HR, steps)?
- How often should export job run (daily, hourly, on-demand)?
- Should we track symptom type patterns (e.g., most common red flags)?

---

### ✅ Next Steps
- Validate schema against tracker + symptom DB
- Implement initial export job
- Set up Power BI workspace + connect to Azure DB
- Draft filters + charts based on this spec