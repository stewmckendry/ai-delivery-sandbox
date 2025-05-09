## 📋 Draft Backlog – Concussion Recovery GPT App (Build Phase)

---

### 🧠 GPT Assistant & Tools

#### 🔹 Structured Triage & Assessment
- [ ] Implement `get_triage_flow` to return full YAML triage map
- [ ] Implement `get_triage_question` for sequential logic
- [ ] Implement `flag_risk` for red flag detection
- [ ] Implement `assess_concussion` to summarize input into structured findings
- [ ] Define custom GPT instructions and memory behavior for triage flow

#### 🔹 Tracker Management
- [ ] Implement `create_tracker` and `update_symptoms` to log user data
- [ ] Implement `get_tracker_status` and `get_tracker_by_code`
- [ ] Add `resume_tracker(tracker_id)` logic and magic link format

#### 🔹 Recovery Stage & Return-to-Play
- [ ] Implement `get_stage_guidance` using `stages.yaml` + symptom/activity inputs

#### 🔹 Clinician Export
- [ ] Implement `export_summary` with support for both PDF and FHIR bundles
- [ ] Connect export to Epic FHIR Observation API

---

### ⚙️ FastAPI Backend & Infra

#### 🔹 YAML Engines
- [ ] Build `triage_engine.py` to parse triage_map.yaml
- [ ] Build `stage_engine.py` to parse stages.yaml and compute stage logic
- [ ] Add YAML validation logic and versioning metadata

#### 🔹 DB & Persistence
- [ ] Design tracker DB and symptom DB schemas
- [ ] Implement DB access layer with SQLite (local) and Azure SQL (prod)

#### 🔹 Wearables Integration
- [ ] Stub `get_wearable_data` with HealthKit sandbox pull or mock generator

#### 🔹 Azure Integration
- [ ] Set up batch export from FastAPI to Azure SQL for Power BI
- [ ] Define export schema (`concussion_dashboard_export`)
- [ ] Connect Power BI and configure slicers, filters, visuals

---

### 📊 Dashboard & Reporting

- [ ] Implement staging job to extract recovery logs to Azure
- [ ] Build Power BI dashboard (filters: sport, age, stage, gender, risk)
- [ ] Test time-based trend graphs and compliance metrics

---

### 🪸 Medical Knowledge Graph

- [ ] Finalize and freeze: `triage_map.yaml`, `stages.yaml`, all `symptoms_*.yaml`
- [ ] Add version control and changelog to YAMLs
- [ ] Ensure compatibility with parsing engines

---

### 🌐 EHR Integration (Epic FHIR)

- [ ] Finalize FHIR app approval process in Epic Sandbox
- [ ] Secure Client ID/Secret and test token exchange
- [ ] Extend `export_summary` to support Observation POST

---

### 📱 UX Enhancements & Exploratory Features

- [ ] Magic link generator + UX for user handoff
- [ ] Enable GPT to support multiple user roles (coach, parent, clinician)
- [ ] TeamSnap integration (stub or research only)
- [ ] Mobile UI shell for embedded GPT

---

### 🔐 Non-Functional Requirements

- [ ] Privacy & anonymization enforcement
- [ ] Logging, monitoring, error handling in FastAPI
- [ ] Testing framework setup (pytest, Postman)
- [ ] OpenAPI schema validation and CI checks