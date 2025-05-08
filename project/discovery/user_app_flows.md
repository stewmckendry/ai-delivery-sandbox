## 👤 User and App Flows – AI Youth Sports Concussion App (PoC)

---

### 👥 User Personas

**1. Parent or Guardian**  
Wants clarity, safety, and step-by-step guidance. Often first to log an incident.  
**2. Coach or Team Staff**  
Needs to confirm status and compliance. Checks player readiness.  
**3. Health Professional**  
Seeks structured data for clinical review. Not always involved at first.  
**4. Sport System Leader**  
Monitors patterns and safety compliance across orgs.

---

### ✈️ Journey Entry Points

1. **New Incident (Assessment Only)**  
2. **Incident + Recovery Tracking**  
3. **Ongoing Recovery Only**  
4. **Clinician Summary Review**  
5. **System Dashboard Monitoring** *(for Sport System Leaders)*

GPT opens with:  
*"Are you logging a new injury or checking in on an existing one?"*

---

### 🔄 Journey A – New Concussion Assessment

| Step | Actor | System | Action | Data | Pre | Post |
|------|-------|--------|--------|------|-----|------|
| 1 | Parent/Coach | GPT | Describes event | Free text | Suspected incident | Start thread |
| 2 | GPT | GPT | Asks guided triage | Prompt logic | - | Capture symptoms |
| 3 | Parent | GPT | Responds to questions | Symptoms | - | Record structured data |
| 4 | GPT + API | Backend | Determine concussion likelihood | Risk flags | - | Start tracker |
| 5 | GPT | GPT | Offers to begin recovery plan | Yes/No | Risk detected | Link to Journey B |
| 6 | GPT | GPT | Shows disclaimer: *Not medical advice* | - | - | Informed consent |

---

### 🏋️‍♂️ Journey B – Ongoing Recovery Check-In

| Step | Actor | System | Action | Data | Pre | Post |
|------|-------|--------|--------|------|-----|------|
| 1 | Parent | GPT | Returns to GPT | Tracker ID | Tracker active | Resume context |
| 2 | GPT | GPT | Asks check-in Qs | Prompt logic | - | Structured inputs |
| 3 | Parent | GPT | Logs symptoms/activity | JSON | - | Store update |
| 4 | GPT + Logic | Backend | Determine recovery stage | Stage = 2/6 | History exists | Stage guidance |
| 5 | GPT | GPT | Shows progress + guardrails | Text, PDF | Risk check | Offer share/export |
| 6 | GPT | GPT | Warns: *Seek care if symptoms worsen* | - | Daily use | Close loop or repeat |

---

### 💼 Journey C – Clinician Summary

| Step | Actor | System | Action | Data | Pre | Post |
|------|-------|--------|--------|------|-----|------|
| 1 | Parent | GPT/API | Shares PDF or FHIR | Export | Appointment | MD gets context |
| 2 | Doctor | EHR | Reviews summary | Timeline | Received | Diagnosis/support |
| 3 | Doctor | Manual | Inputs clearance (optional) | Status | Visit done | Final stage set |

---

### 📊 Journey D – System Dashboards

| Step | Actor | System | Action | Data | Pre | Post |
|------|-------|--------|--------|------|-----|------|
| 1 | Admin | Azure | Views dashboard | JSON log | At least 1 case | Insight view |
| 2 | Admin | Azure | Filters by sport, age, etc. | Filters | - | Pattern awareness |

---

### 🔌 Systems of Interaction

| System | Role |
|--------|------|
| **ChatGPT (Custom GPT)** | Conversational interface + logic bridge |
| **FastAPI Backend** | Handles logic, stores structured recovery data |
| **Epic FHIR Sandbox** | Receives structured export for clinicians |
| **Apple HealthKit / Google Fit** | (Mocked) activity data for recovery stage |
| **Azure Dashboard** | Aggregated system insights |

---

### ⚠️ Guardrails + Consent

- GPT declares: *"This is not medical advice. Talk to a doctor if in doubt."*
- If danger signs: *"Stop and call a professional now."*
- Symptoms like LOC, vomiting, neck pain trigger diversion to emergency guidance.

---

### 🧪 PoC Experimentation Access

| Element | Plan |
|---------|------|
| GPT Interface | Shared Custom GPT link with intro and guardrails |
| Backend | Hosted FastAPI with open endpoints for PoC use |
| Epic EHR | Use public FHIR sandbox with sample patients |
| Azure | Basic dashboard reading mock data from backend |

**Design Notes:**
- No login, session ID or link-based resume
- No PHI collected
- Data is fake/sample only
- Simple rate limiting or alerts to catch misuse

---

### 🔍 Exploration Note

As part of the PoC, we may also explore potential integration with popular team sports management platforms like **TeamSnap** to provide a more connected experience for coaches and teams. This could include auto-notifying rosters or syncing player status. While not required for the PoC, research and documentation of opportunities will be included.

---

### ⚖️ Assumptions

- Open Epic FHIR sandbox is sufficient
- Parents can resume via link/memory
- Custom GPT supports state context via backend
- Users can consent via GPT intro text
- No auth needed in PoC

---

### 🔗 Connected Flow View

1. GPT asks entry question (new vs check-in)  
2. All flows route through the same structured backend  
3. EHR and dashboard pull from same store  
4. Recovery tracker follows user regardless of path in  
5. Safety net messages and branching ensure risk routing