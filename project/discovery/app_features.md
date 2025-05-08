## 🔧 App Feature Breakdown – Concussion Recovery GPT App (PoC)

---

### 🔢 Feature Summary Table (By Category)

| Category                | Feature                           | Tool/API Name                           | Journey | Priority |
| ----------------------- | --------------------------------- | --------------------------------------- | ------- | -------- |
| GPT Assistant           | Structured Triage & Assessment    | `get_triage_question`, `create_tracker` | A       | High     |
|                         | Return-to-Play Guidance           | `get_stage_guidance`                    | B       | High     |
|                         | Emergency Risk Detection          | `flag_risk`                             | A, B    | High     |
|                         | Log Daily Recovery Updates        | `update_symptoms`                       | B       | High     |
|                         | Resume Tracker Context            | `get_tracker_status`                    | B       | High     |
|                         | Export Summary for Clinicians     | `export_summary`                        | C       | Medium   |
|                         | Fetch Wearable Data               | `get_wearable_data`                     | B       | Medium   |
| Backend Systems         | Store Tracker                     | `create_tracker`                        | A       | High     |
|                         | Symptom Log & Stage Inference     | Stage Engine + DB                       | B       | High     |
|                         | Export Formatter (FHIR/PDF)       | `export_summary`                        | C       | Medium   |
| Medical Knowledge Graph | SCAT6 Staging, Symptoms, Triggers | Embedded YAML/JSON                      | A, B    | High     |
| EHR Integration         | Push FHIR Export to Epic          | REST/FHIR API                           | C       | Medium   |
| Azure Dashboard         | Visualize Aggregate Recovery Data | Azure Power BI                          | D       | Medium   |
| Wearables               | Fetch Mock Activity Data          | `get_wearable_data`                     | B       | Medium   |

---

### 🧠 Medical Knowledge Graph

#### Mock Schema Example

```yaml
triage_flow:
  initial_prompt: "Can you describe what happened?"
  follow_ups:
    - if: "mentions hit or collision"
      then: "Did they lose consciousness or feel dizzy?"
    - if: "mentions headache"
      then: "On a scale of 1-10, how bad is it?"

symptom_thresholds:
  dizziness: severe
  vomiting: immediate
  unconscious: immediate

concussion_stages:
  stage_1:
    description: "Symptom-limited activity"
    criteria:
      symptoms: [headache, fatigue]
      activity: "low"
  stage_2:
    description: "Light aerobic exercise"
    criteria:
      symptoms: [mild only]
      steps_min: 2000
```

* **Storage**: Stored as structured YAML or JSON in backend (e.g., `stages.yaml`, `symptoms.yaml`, `triage_map.yaml`)
* **Schemas**:

  * `concussion_stages`: maps SCAT6 recovery stages to symptoms and activity rules
  * `symptom_thresholds`: flags danger triggers
  * `triage_flow`: maps symptoms to structured triage prompts and follow-ups
* **Access**:

  * GPT uses this via backend lookups or in-memory context
  * Backend tools (e.g., Stage Engine, `flag_risk`) use this for logic

---

### ⌚ Wearable Devices (Mocked)

* **Storage**: Mock step/sleep/HR data pulled from Apple HealthKit or Google Fit sandbox mode
* **Access**:

  * GPT calls `get_wearable_data` tool
  * Backend generates mock data if not available
* **Schema**:

```json
{
  "user_id": "abc123",
  "date": "2024-05-01",
  "steps": 4200,
  "sleep_hours": 7.5,
  "resting_hr": 68
}
```

* **Use**: Helps assess activity stage in recovery guidance

---

### ⚙️ Technology Utilities

* **FastAPI App**: Hosts OpenAPI endpoints (tools) and internal utility functions
* **Symptom DB**: Internal DB (not EHR) that logs symptom check-ins for analytics/export; structured by tracker ID, timestamp, symptoms
* **Azure DB**: Stores de-identified tracker logs for analysis by Power BI dashboard; includes recovery stages, timestamps, optional filters
* **EHR**: Only receives structured export (PDF or FHIR bundles), not raw DB (PDF or FHIR bundles), not raw DB

---

### ✈️ Journey Details & Tool Mapping

GPT accesses triage\_flow and stages.yaml via OpenAPI tools:

* `get_triage_question`: Returns next triage prompt from triage\_flow\.yaml based on previous input
* `get_stage_guidance`: Evaluates symptoms and wearable data against stages.yaml to return current recovery stage and guidance

These tools can be chained automatically within the GPT to enable a fluid chat while producing structured outputs.

Tracker is a persistent user-specific log stored in the Symptom DB. It includes:

* Incident metadata, daily symptoms, stage progression
* Select data is exported to FHIR (Condition, Observation, CarePlan)

Logs are exported to Azure on a scheduled batch process (e.g., every 24 hours), enabling system-level analysis.

#### 1. New Incident (Assessment Only)

* **Preconditions**: Parent/coach opens GPT; reports an incident
* **Steps**:

  1. GPT opens with *"Tell me what happened"*
  2. GPT uses `triage_flow` graph to ask follow-up questions
  3. Symptoms matched against `symptom_thresholds`
  4. If dangerous → `flag_risk` tool triggered
  5. If concussion likely → GPT calls `create_tracker`
  6. GPT provides basic concussion guidance (not diagnosis)
* **Postconditions**: Tracker created, guidance shared, optionally continue into Journey 2

#### 2. Incident + Recovery Tracking

* **Preconditions**: Tracker was created or resumed
* **Steps**:

  1. GPT welcomes user back, calls `get_tracker_status`
  2. GPT prompts symptom check-in → user logs via `update_symptoms`
  3. GPT calls `get_wearable_data` for recovery insight
  4. Stage Logic Engine uses `stages.yaml` to infer recovery stage
  5. GPT gives next-step recovery guidance
* **Postconditions**: Tracker updated, next check-in prompt prepared

#### 3. Ongoing Recovery Only

* **Preconditions**: User resumes journey (tracker ID stored)
* **Steps**:

  1. GPT fetches tracker using `get_tracker_status`
  2. Asks daily check-in → logs via `update_symptoms`
  3. Stage + wearable check used to refine guidance
* **Postconditions**: Recovery updated, readiness assessed

#### 4. Clinician Summary Review

* **Preconditions**: User chooses to export tracker
* **Steps**:

  1. GPT calls `export_summary`
  2. Output is rendered to PDF or FHIR JSON
  3. User can download PDF or GPT pushes JSON to Epic FHIR API
* **Postconditions**: Clinician has structured data for diagnosis or clearance

#### 5. System Dashboard Monitoring

* **Preconditions**: Recovery logs exist in system
* **Steps**:

  1. Azure dashboard queries backend logs (de-identified)
  2. Visualizes stage distribution, avg recovery days, incidents over time
  3. Admin filters by sport, gender, age
* **Postconditions**: Safe Sport reports and trends visible

---

### 🔐 Non-Functional Requirements

* **Privacy & Security**: While we collect personal health information (PHI) such as symptoms and incident details, all data is stored using anonymized identifiers. No names, addresses, or direct identifiers are collected. Exported data is user-initiated and can be shared with healthcare providers under user control.
* **Monitoring**: FastAPI logs interactions; GPT errors tracked via OpenAI usage reports
* **Cloud Infrastructure**: Azure-hosted backend with daily export jobs; uses GitHub + GitHub Actions for CI/CD; scalable storage for tracker logs

### 🧱 Build Order (Updated)

1. **GPT Setup + Triage Engine**

   * Instructions, `create_tracker`, `flag_risk`, `triage_flow.yaml`
2. **Daily Logging + Memory**

   * `update_symptoms`, `get_tracker_status`, symptom DB, `stages.yaml`
3. **Wearable and Stage Engine**

   * `get_wearable_data`, Stage rules, recovery UX
4. **Clinician Export + EHR Push**

   * `export_summary`, FHIR mapping, Epic integration
5. **Azure Dashboard Setup**

   * Log aggregation, Power BI embed, Safe Sport filters
6. **Exploratory Features**

   * TeamSnap stub, multi-user sharing, mobile UI