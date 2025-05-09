## 👤 User Journey Entry Points – Tracker Metadata + Tools

This note outlines how we support various user entry points using the current system design.

---

### 1️⃣ Incident-First Flow (Initial Reporting)
**User just had an incident and wants to check for concussion**

- Entry Tool (planned FA7): `log_incident_detail`
- Data: `injury_date`, `reporter_role`, `incident_context`
- Outcome: Creates `tracker_metadata` with context
- Then: Flow proceeds to `get_triage_flow` → guided screening

📥 Will support YAML-linked context fields
📌 Required for system-wide data completeness

---

### 2️⃣ Symptom Follow-Up Flow
**User returns after incident to update symptoms**

- Entry Tool: `/log_symptoms`
- Outcome: Updates `symptom_log`, updates `tracker_metadata`
- Then: Optionally calls `/get_stage_guidance`

🟢 Fully supported today

---

### 3️⃣ Retroactive Recovery Check
**User had an old incident and never reported it, wants return-to-play guidance**

- Entry: Starts with `log_symptoms`, using backdated `injury_date`
- Outcome: Infers current stage using `get_stage_guidance`

⚠️ Works today, but we may want a tailored prompt path for this case

---

### 🔁 System Links
- All 3 flows generate or rely on `TrackerMetadata`
- `tracker_metadata` supports persistence, export, and stage logic
- `symptom_log` is append-only; `tracker_metadata` is per-user summary

---

### 📍 Status
- Flow (2) is implemented
- Flow (1) and Flow (3) supported by tooling but require experience design and task scaffolding
- `log_incident_detail` scoped to FA7

---