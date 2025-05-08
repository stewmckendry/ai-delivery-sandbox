## ✅ Acceptance Criteria – Concussion Recovery GPT App

---

### 🧠 GPT Tools

#### `get_triage_flow`
- Returns the full triage question set defined in triage_flow.yaml
- GPT is expected to iterate through these conversationally
- Used to preload all relevant prompts into memory context

#### `assess_concussion`
- Evaluates structured symptoms against symptom_thresholds
- Determines if concussion is likely based on symptom count and severity
- Used between triage Q&A and tracker creation
- Outputs boolean (likely/not likely) and a reasoning summary

#### `get_triage_question`
- (Deprecated in favor of `get_triage_flow`)
- Previously returned next triage question based on current context
- Replaced by GPT-driven loop through full prompt set

#### `create_tracker`
- Creates a new recovery tracker entry tied to a unique user/session ID
- Stores incident time, key symptoms, and initiates stage 1 in DB
- Confirms tracker created and offers to begin recovery tracking
- Fails gracefully if tracker already exists for user/session

#### `flag_risk`
- Evaluates structured symptoms and flags if any threshold in symptom_thresholds.yaml is triggered
- Triggers immediate warning with recommendation to seek clinical care
- Should log risk flag in tracker metadata

#### `get_stage_guidance`
- Fetches current symptoms and activity level from tracker
- Applies stages.yaml to compute current stage
- Returns stage name, guidance summary, and next expected step
- Edge case: if data is incomplete, suggests a symptom check-in first

#### `update_symptoms`
- Adds symptom data to existing tracker entry for the current day
- Accepts flexible input (text or form-style data)
- Confirms update and provides summary of status
- Logs timestamp and deltas vs. last entry

#### `get_tracker_status`
- Retrieves latest tracker record for user
- Includes stage, last update time, symptom trend
- Returns null/404 if no tracker exists for user

#### `export_summary`
- Formats tracker data into PDF and/or FHIR JSON
- PDF includes user-readable timeline, symptom history, and stage changes
- FHIR includes Condition, Observation, CarePlan objects
- Edge case: prompts user to complete missing entries before export

#### `get_wearable_data`
- Retrieves mock or sandbox wearable data for most recent 1-3 days
- Accepts user ID or tracker ID
- Returns daily steps, sleep hours, resting HR
- Fallback: generates synthetic data if real data unavailable

---

### 🗄️ System Components

#### Apple Health (Mock Sandbox)
- Simulates wearable data via HealthKit sandbox
- Provides mock steps, HR, and sleep values for 1–3 recent days
- Source for `get_wearable_data` fallback generator

#### Symptom DB
- Stores tracker records in anonymized, timestamped format
- Indexed by user ID and date
- Must support filtering by stage, sport, gender for analytics

#### Azure DB
- Receives daily export from Symptom DB (batch job)
- Includes stage, symptom score, time in stage
- Export must scrub personal IDs and format for dashboard ingest

#### EHR Integration (Epic FHIR)
- Receives export from `export_summary` tool (FHIR format)
- Must confirm delivery or raise failure
- Supports one-click push from GPT or manual download/upload

#### Azure Dashboard
- Displays Safe Sport trends (concussion rate, avg recovery time)
- Supports filters by org, sport, gender, date
- Visualizes stage distribution and system flag rates

---

### 📱 User Interaction

#### Triage Journey
- Starts with natural language input
- Proceeds through Q&A aligned to triage_flow
- Concludes with summary of risk and option to create tracker

#### Recovery Journey
- Prompts daily check-ins
- Combines `update_symptoms` and `get_stage_guidance`
- Gives stage-aware return-to-play advice
- Shows status on request via `get_tracker_status`

#### Export Journey
- Asks if user wants to export report
- Confirms and presents PDF preview + push to Epic option
- Can retry if user updates missing data

#### Monitoring Journey
- Admin accesses Azure Dashboard
- Filters and explores de-identified trends
- Can export dashboard view as report

---

More criteria will be added for exploratory features and edge integrations in future tasks.