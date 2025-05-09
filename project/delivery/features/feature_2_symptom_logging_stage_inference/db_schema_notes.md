## 🗃️ DB Schema – Symptom Logging & Tracker Metadata

This schema note outlines proposed structures for persistence in Feature Area 2.

---

### ✅ Symptom Log Table
Stores one entry per user check-in.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique record ID |
| user_id | str | User performing check-in |
| checkin_time | datetime | Timestamp of check-in |
| symptoms | JSON | Dict of symptom_id → 0–5 severity |
| stage_inferred | str | Optional stage result from engine |
| source | str | GPT/manual/input channel |

- Indexed on `user_id`, `checkin_time`
- Used for audit trail and export

---

### ✅ Tracker Metadata Table
Stores persistent context for each user.

| Field | Type | Description |
|-------|------|-------------|
| user_id | str | Unique user identifier |
| injury_date | date | When injury occurred |
| last_stage_id | str | Last stage inferred by engine |
| cleared_to_play | bool | Flag indicating play clearance |
| last_checkin_time | datetime | Most recent check-in timestamp |

- One row per user
- Referenced in tool calls and staging logic

---

### 💡 Builder Notes
- Initial implementation may use SQLite (or mock JSON)
- Use ORM or Pydantic-sql for alignment
- Align with `TrackerState`, `SymptomCheckIn` schemas

---

### ☁️ Azure SQL Integration
These tables will be exported and used in Azure-based dashboards and reports in Feature Area 5:

- `symptom_log` → time-series trends, red flag frequency, symptom evolution
- `tracker_metadata` → recovery tracking, funnel metrics, return-to-play analytics
- Export via batch script or pipeline (CSV/JSON)
- Aligned with Power BI spike format

---

### 📈 Future Enhancements
We plan to extend these tables with contextual incident metadata for richer system-level insights. Example fields:

- `sport_or_activity`: e.g. soccer, football, cycling
- `injury_context`: e.g. game, practice, fall, unknown
- `reporter_role`: e.g. self, coach, parent, clinician

This will support:
- Epidemiology studies
- Risk profiling by activity
- Policy feedback and trend analysis

Implemented in: Feature Area 7 or 8 (incident detail capture + analysis)

---

### 🔗 Related Features
- Used by: `symptom_logger`, `get_stage_guidance`
- Extended in: Feature 5 (dashboards), Feature 8 (multi-user)

---