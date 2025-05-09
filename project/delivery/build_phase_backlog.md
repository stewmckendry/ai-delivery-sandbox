## 📋 Delivery Backlog – Concussion Recovery GPT App (PoC)

---

### 🧠 FEATURE AREA 1 – Triage + Concussion Assessment

#### 🎯 Goals
- Enable guided triage with YAML logic and red flag detection
- Assess concussion likelihood based on user input
- Initiate recovery tracker if needed

#### 🔨 Includes
- `get_triage_flow`, `get_triage_question`
- `flag_risk`, `assess_concussion`
- `create_tracker`
- GPT instructions for triage and guidance delivery
- Prompt schema design and fallback behavior

#### 🔍 Mapped Backlog Items
- Structured Triage & Assessment
- Tracker Management (part)
- YAML Engines (triage)

---

### 📅 FEATURE AREA 2 – Symptom Logging + Stage Inference

#### 🎯 Goals
- Enable daily check-ins with symptom tracking
- Infer recovery stage and give return-to-play guidance

#### 🔨 Includes
- `update_symptoms`, `get_tracker_status`, `get_stage_guidance`
- `stage_engine.py`, symptom DB
- Resume tracker logic + magic link
- GPT prompt tuning for recovery updates

#### 🔍 Mapped Backlog Items
- Tracker Management (rest)
- Recovery Stage Logic
- YAML Engines (stage)
- Session Memory / Resume UX

---

### 📦 FEATURE AREA 3 – Wearables Integration + Guidance

#### 🎯 Goals
- Incorporate mock wearable data into stage logic and recovery decisions

#### 🔨 Includes
- `get_wearable_data`
- FastAPI logic for mock data generation

#### 🔍 Mapped Backlog Items
- Wearables Integration (PoC only)

---

### 🏥 FEATURE AREA 4 – Clinician Export (PDF + FHIR)

#### 🎯 Goals
- Allow users to export structured summaries of recovery
- Send to Epic FHIR sandbox or as PDF

#### 🔨 Includes
- `export_summary` tool (PDF + FHIR)
- `epic_writer.py`, `epic_client.yaml`
- FHIR write stub for future pull support

#### 🔍 Mapped Backlog Items
- Clinician Export
- EHR Integration

---

### 📊 FEATURE AREA 5 – Azure Dashboard + Data Export

#### 🎯 Goals
- Aggregate recovery logs for Power BI dashboards

#### 🔨 Includes
- Azure SQL staging schema (`concussion_dashboard_export`)
- FastAPI export job
- Power BI dashboard setup (filters, charts)

#### 🔍 Mapped Backlog Items
- Azure Integration
- Dashboard & Reporting

---

### ⚙️ FEATURE AREA 6 – YAML Engines + Tool Contracts

#### 🎯 Goals
- Ensure consistent YAML logic parsing and schema control
- Serve as foundation for Feature Areas 1 & 2

#### 🔨 Includes
- `triage_engine.py`, `stage_engine.py`
- YAML schema validation and changelogs
- YAML versioning and changelog enforcement
- OpenAPI tool specs for all tools

#### 🔍 Mapped Backlog Items
- YAML Engines
- Medical Knowledge Graph
- Non-Functional: CI, validation

---

### 🧪 FEATURE AREA 7 – Testing, Security, and Infra Readiness

#### 🎯 Goals
- Ensure backend quality, observability, test coverage, and basic security

#### 🔨 Includes
- Pytest suite for FastAPI tools
- Postman contract tests
- Logging, monitoring, error handling
- GPT-level observability (tool usage, fallback, red flag rates)
- Anonymization, HTTPS, no PHI in logs
- Magic link expiry, rate limiting, token security

#### 🔍 Mapped Backlog Items
- Testing Framework
- Logging/Monitoring
- Security & Privacy
- OpenAPI validation

---

### 💡 FEATURE AREA 8 – UX Enhancements & Exploratory Work

#### 🎯 Goals
- Improve PoC polish and explore future UX capabilities

#### 🔨 Includes
- Magic link generation and guidance for resuming sessions
- GPT role-based flows for parent, coach, clinician
- TeamSnap integration (stub or research only)
- FHIR pull/read stub (out of PoC scope)

#### 🔍 Mapped Backlog Items
- UX Enhancements
- Exploratory Features

> Note: Mobile UI shell replaced by Custom GPT front-end. No custom UI needed in PoC.

---

### 🧭 FEATURE AREA 9 – Conversational Agent as App Layer

> This feature generalizes the approach used in Feature Area 1, showing how guided triage and structured workflows can evolve into a broader architecture where the agent fully replaces app logic.

#### 🎯 Goals
- Demonstrate that a conversational agent can replace traditional forms and static apps
- Use structured, tool-driven workflows coordinated entirely by the agent
- Show domain transferability of the pattern

#### 🔨 Includes
- Design an additional agent-led flow (e.g., school nurse intake, post-game wellness check)
- Ensure the agent:
  - Collects data conversationally
  - Calls YAML tools and DB functions
  - Outputs structured results or exports
- Instructions and tooling that generalize to other domains

#### 🔍 Mapped Backlog Gaps Filled
- Prompt orchestration and workflow chaining
- Agent-as-UI pattern
- Multi-tool coordination by LLM
- Pattern portability across verticals