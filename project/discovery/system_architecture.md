## 🧱 System Architecture & Engineering Standards – Concussion Recovery GPT App (PoC)

---

### 🧭 Overview
This architecture outlines how we will implement an AI-native concussion support system using a Custom GPT frontend and a modular, API-first backend. It integrates medical logic, third-party systems (EHR, Apple Health, Azure), and end-user experiences (parents, clinicians, coaches, system leaders).

---

### 🧰 Tech Stack by Component

| Layer              | Tech                     | Description                                 |
|-------------------|--------------------------|---------------------------------------------|
| Frontend (UI)     | OpenAI Custom GPT        | Conversational UI for triage and recovery   |
| Backend Core      | FastAPI (Python)         | Hosts GPT tools and logic engine            |
| API Interface     | OpenAPI schema           | Contract between GPT and backend            |
| Data Storage      | SQLite / Azure SQL       | Tracker logs, symptoms, wearable snapshots  |
| Dashboard         | Azure Power BI           | Aggregated insights for system monitoring   |
| EHR Integration   | FHIR (Epic API)          | Push summary data to clinician systems      |
| Wearables         | Apple HealthKit Sandbox  | Simulated data for steps, HR, sleep         |
| Knowledge Graph   | YAML files               | Medical rules (triage, symptoms, stages)    |
| CI/CD             | GitHub + GitHub Actions  | Versioned deploy to Azure backend           |

---

### 🔗 Interfaces & Contracts

### 📜 OpenAPI Schema
The OpenAPI schema defines the contract between Custom GPT and the FastAPI backend. It includes paths for each tool:
- `/create_tracker`
- `/flag_risk`
- `/update_symptoms`
- `/get_tracker_status`
- `/get_stage_guidance`
- `/export_summary`
- `/get_wearable_data`
- `/get_triage_flow`
- `/assess_concussion`

Each tool has:
- A description (purpose and input/output structure)
- Request/response schemas
- Authentication flag (none for PoC)

Schema will be versioned and used in both backend (FastAPI) and GPT tool config.
- **Custom GPT ↔ FastAPI** via OpenAPI tools
- **FastAPI ↔ YAML** via logic engine (in-memory load)
- **FastAPI ↔ Azure SQL** via SQLAlchemy
- **FastAPI ↔ FHIR (Epic)** via REST POST to clinician endpoint
- **FastAPI ↔ Azure Power BI** via export job to Azure Blob / DB
- **FastAPI ↔ Apple HealthKit** (simulated fetch for mock data)

---

### 🗃️ Data Schemas

### 📦 YAML File Storage
- YAML files are accessed from the current GitHub repo (`ai-delivery-sandbox`) and active branch (`sandbox-silver-tiger`)
- All medical knowledge graph YAMLs (`triage_map.yaml`, `stages.yaml`, `symptoms_*.yaml`) are stored in the `reference/` folder
- FastAPI loads these files at startup into memory and serves logic tools
- YAMLs are versioned in Git and validated for schema consistency
- **User Tracker (DB)**: `user_id`, `symptoms[]`, `stage`, `daily_logs`, `flags`, `exports[]`
- **FHIR Export**: Observation, Condition, CarePlan JSON bundle
- **YAML Logic**: `triage_map.yaml`, `symptoms_*.yaml`, `stages.yaml`
- **Wearable Mock**: JSON: `steps`, `sleep`, `HR`, `timestamp`

---

### 🌐 External System Setup
- **Apple Health**: HealthKit sandbox setup to simulate fitness data
- **EHR (Epic)**: Use FHIR Developer Sandbox with preloaded patients
- **Azure**: Host DB and Power BI dashboard; enable blob export

---

### 🧠 Custom GPT Design
- **Instructions**: Include role, scope, safety, escalation rules
- **Tools** (via OpenAPI): `create_tracker`, `flag_risk`, `update_symptoms`, `get_tracker_status`, `get_stage_guidance`, `export_summary`, `get_wearable_data`, `get_triage_flow`, `assess_concussion`
- **Memory**: Tracker and stage history linked to session ID

---

### ☁️ Cloud Deployment

### 📄 Licensing & Subscriptions
- **OpenAI Custom GPT**: Free for GPT builder; may require ChatGPT Plus ($20/mo) for external testers
- **Azure**: Use free tier for Web App, SQL DB, and Power BI (subject to usage limits)
- **Epic Sandbox**: Free developer access to FHIR API
- **Apple HealthKit**: Free sandbox mode available for developer testing
- **GitHub Actions**: Free for public repos or low-usage projects
- Azure Web App for FastAPI backend
- SQLite in dev, Azure SQL in prod
- Nightly Azure blob export for Power BI

---

### 🔧 Development Standards
- **Versioning**: Semantic versioning per tool and OpenAPI schema
- **Testing**: Pytest for FastAPI; Postman collection for API contract
- **Security**: No PHI in logs, anonymized exports, HTTPS only
- **Docs**: Code must be documented inline and in tool YAML
- **Code Review**: GitHub PRs with CI checks

---

### 🧭 Mapping Features to Systems
| Feature                     | Component(s) Used                          |
|----------------------------|-------------------------------------------|
| Triage + Symptom Intake    | GPT + `get_triage_flow`, `flag_risk`, YAML|
| Concussion Likelihood      | `assess_concussion` + symptom YAML        |
| Tracker Creation           | `create_tracker` + Symptom DB             |
| Daily Updates              | `update_symptoms` + Wearable + YAML       |
| Return-to-Play Guidance    | `get_stage_guidance` + stage rules        |
| Export to Clinician        | `export_summary` + FHIR API               |
| System Dashboard           | Azure export + Power BI                   |

---

### 🔍 Assumptions & Spikes
- 🟢 Assume sandbox access to Apple + Epic is available
- 🟡 Spike: authorization for writing to Epic sandbox
- 🟡 Spike: YAML inference in GPT flow for triage
- 🟡 Spike: design of Power BI filters and staging pipeline
- 🟡 Spike: feasibility of session memory linking across visits

---

### ✅ Ready to Spec & Build
- All tools defined
- Interfaces mapped
- Clinical YAML logic complete
- Feature → tool → system traceability ready