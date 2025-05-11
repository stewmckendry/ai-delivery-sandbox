## 📊 Dashboard Flow – Feature 5: Azure Export to Power BI

### 🎯 Audience
Sports system leaders looking to understand:
- Concussion incident trends
- Recovery stage distributions
- Return-to-play patterns across programs

---

### 🔁 Export Pipeline
1. `export_to_sql.py` reads:
   - Tracker + symptom log data from DB
   - YAML maps from GitHub (triage, stages)
2. Writes to Azure SQL:
   - `tracker_export`
   - `symptom_log_export`
3. Tables are made readable by Power BI

---

### 📊 Dashboard Concepts
- **Recovery Funnel**: # of users in each stage
- **Symptom Trendline**: severity over time
- **Red Flag Alert Rate**: frequency of triage hits
- **RTS Delay**: time from incident to Stage 5
- **Demographic Filter** (if data available): gender, sport, team

---

### 🔐 Access
- DB login via secure credentials
- Optionally use Azure Synapse for integration at scale

---

Export can run on schedule (e.g. daily) or ad-hoc via CLI.