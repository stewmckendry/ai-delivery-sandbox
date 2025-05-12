## 📋 Feature Scope Tracker – Build Phase

This document tracks scope definitions, adds, and changes across all feature areas.
Update after each feature delivery or when scope changes during build.

---

### 🧠 Feature Area 1 – Triage + Concussion Assessment
**Status**: Done

✅ Core Scope
- Guided flow using YAML triage map
- Tracker state building via Custom GPT

📥 Added During Build
- `get_triage_flow` (full map load in one call)
- Tracker state handling and question ID mapping

📤 Deferred
- Dynamic risk scoring logic → FA5

---

### 📅 Feature Area 2 – Symptom Logging + Stage Inference
**Status**: Done

✅ Core Scope
- Log symptom check-ins
- Infer stage via `stage_engine`
- TrackerState schema + GPT integration

📥 Added During Build
- YAML validation of symptoms
- DB schema notes for persistence
- Tool contracts for Custom GPT
- Switched DB write integration from SQLite to direct Azure SQL (SQLAlchemy)

📤 Deferred
- Symptom score rollups → FA5
- Incident context fields (e.g., activity, reporter) → FA7/8

---

### 📦 Feature Area 3 – Wearables Integration + Guidance
**Status**: Not Started

✅ Core Scope
- Accept timestamped wearable check-ins
- Use in recovery guidance

📥 Proposed
- FastAPI for mock sensor input
- Normalize schema for stage analysis

📤 Deferred
- Continuous monitoring loop → FA8

---

### 🏥 Feature Area 4 – Clinician Export (PDF + FHIR)
**Status**: Done

✅ Core Scope
- Summarize tracker data for export
- Support Epic FHIR sandbox + PDF output

📥 Added During Build
- `export_summary`, `epic_writer`, `pdf_renderer`
- Azure Blob upload + signed SAS delivery
- FHIR and PDF flow notes
- Full test coverage and tool traceability

📤 Deferred
- Real FHIR pull support → post-PoC

---

### 📊 Feature Area 5 – Azure Dashboard + Data Export
**Status**: In Progress

✅ Core Scope
- Sync tracker + symptom logs to Azure SQL
- Prototype Power BI dashboard

📥 Proposed
- Time-series trends, flag frequencies
- Contextual metadata integration
- Dynamic risk scoring logic (from FA1)
- Symptom score rollups (from FA2)
- New tools: `log_incident_detail`, `get_triage_flow`, `get_triage_question`, `assess_concussion`, `log_symptoms`, `get_stage_guidance`, `export_summary`
- `main.py` + OpenAPI + FastAPI router

📤 Deferred
- Longitudinal views and filters → FA8

---

### ⚙️ Feature Area 6 – YAML Engines + Tool Contracts
**Status**: Done

✅ Core Scope
- `triage_engine`, `stage_engine`
- YAML schema validator
- OpenAPI tool specs

📥 Added During Build
- YAML validator CLI
- Example-driven schema comments

📤 Deferred
- Multi-language YAML support → FA7

---

### 🧪 Feature Area 7 – Testing, Security, Infra
**Status**: Not Started

✅ Core Scope
- Unit + contract test coverage
- Logging and GPT observability
- Security (magic links, HTTPS, PHI policy)

📥 Proposed
- Pytest + Postman test flows
- Token limits, expiry, rate limiting
- Incident context fields (e.g., activity, reporter) (from FA2)
- Multi-language YAML support (from FA6)
- New tool: `log_incident_detail` (explicit reporting of incident before symptoms)
- Support for user journey entry points 1–3

📤 Deferred
- Role-based RBAC + data walls → FA8

---

### 💡 Feature Area 8 – UX Enhancements & Exploratory
**Status**: Not Started

✅ Core Scope
- Multi-role flows (coach, clinician)
- Magic link guidance

📥 Proposed
- TeamSnap stub, GPT profile modes
- Role-based UI views
- Continuous monitoring loop (from FA3)
- Longitudinal cohort filters (from FA5)
- Role-based RBAC + data walls (from FA7)

📤 Deferred
- Advanced UX shell → replaced by Custom GPT

---

### 🧭 Feature Area 9 – Conversational Agent as App Layer
**Status**: Not Started

✅ Core Scope
- Generalize triage pattern to other flows
- Replace forms with agent-led sequences

📥 Proposed
- Intake examples (e.g., nurse, game check)
- YAML + tracker use in new domains

📤 Deferred
- Auto-configuration tools for vertical reuse

---