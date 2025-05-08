# Project Summary: AI-Powered Youth Sports Health App (Concussion Use Case)

---

## Mission

To help families, coaches, and health systems better manage sports injuries — starting with concussions — by combining easy-to-use AI guidance with structured tracking, personalized insights, and evidence-based recovery support.

---

## What Inspired It

This app was born from real challenges seen on the field and in the clinic:

- **Parents and coaches struggle to know what counts as a concussion**  
  “My head hurts” — is it serious or not? Most aren’t trained to assess injuries confidently.

- **Recovery guidance is confusing and inconsistent**  
  After an injury, families are left asking: *What can my child do? When can they go back? Is it safe?*

- **There’s growing demand for structured sports injury reporting**  
  Sport organizations and governments need data to track trends, improve safety, and design better return-to-play protocols.

- **Health professionals are often left out of the loop**  
  Doctors may only see partial info — or none at all — making it harder to give the right advice.

---

## What We're Building

An AI-powered app that:

- Walks parents and coaches through a concussion assessment in plain language  
- Logs symptoms, activity, and recovery progress  
- Provides personalized guidance based on recognized medical protocols  
- Shares structured updates with doctors or sport organizations  
- Tracks trends to help health systems and governing bodies improve care and prevention  

This isn’t just another form or chatbot. It’s a smart assistant that helps the right people take the right actions — at the right time.

---

## Who It's For

### 1. Parents and Guardians
- Report injuries quickly and accurately  
- Get simple, personalized advice at each step  
- Track when it’s safe to return to play

### 2. Coaches and Team Staff
- Understand if and when a player is ready  
- Ensure everyone follows safe sport protocols  
- Share updates with families or health teams

### 3. Health Professionals
- See structured injury details before a visit  
- Review symptom history and activity trends  
- Align care with real-world recovery steps

### 4. Sports System Leaders (e.g., Sport Canada, PSOs)
- Monitor concussion rates and recovery patterns  
- Generate Safe Sport reports with real data  
- Design better policies and prevention programs

---

## User Journeys (Examples)

- A **parent logs an injury** → answers a few guided questions → app suggests a likely concussion and starts a recovery tracker  
- A **coach checks recovery status** → sees the player is on Stage 3 of 6 → confirms readiness before returning to drills  
- A **doctor receives a summary** → reviews symptoms, timelines, and wearable data → confirms return-to-play safety  
- A **sport system administrator pulls a quarterly report** → sees concussion trends by sport and age group → updates safety guidelines

---

## What Powers It (Tech Stack)

- **Custom ChatGPT front end**  
  Natural conversation guides users through injury logging, questions, and personalized recommendations

- **FastAPI backend**  
  Applies medical logic, processes user input, and stores structured records

- **EHR Integration (e.g., Epic, Cerner via FHIR)**  
  Shares injury and recovery details directly with doctors via the electronic health record system

- **Wearable Device Integration (e.g., Apple HealthKit, Google Fit)**  
  Tracks real-world activity (like steps, sleep, heart rate) to support safe recovery and guide return-to-play

- **Azure Cloud**  
  Securely stores all data, supports dashboards and reporting, and enables analytics for sport organizations and clinicians

- **Medical Knowledge Graph**  
  Encodes return-to-play protocols (like SCAT6) and symptom logic, helping the AI reason through what stage the player is in and what to do next

---

## Why It’s Better

| User            | Benefit vs. Traditional Forms or ChatGPT Alone                      |
|-----------------|---------------------------------------------------------------------|
| **Parent**      | No guesswork — clear guidance tailored to their child and sport     |
| **Coach**       | One place to check status and follow protocol — no paper, no confusion |
| **Clinician**   | Structured, accurate data before appointments — faster, better care |
| **System Leader** | Trustworthy data for reporting and decision-making at scale      |

Unlike traditional forms or standalone ChatGPT, this system combines AI reasoning with structured workflows, medical logic, and real-time data — creating a smarter, safer experience.

---

## Risks and Considerations

- **Privacy and consent**: Health and youth data must be handled with care and full transparency  
- **Access and equity**: Not all families have wearable devices or comfort with digital tools  
- **Clinical alignment**: Guidance must reflect trusted medical protocols and stay up to date  
- **Over-reliance on AI**: This is a guide — not a replacement for doctors or parental judgment

---

## Scope for PoC: What's In vs. Out

### ✅ IN SCOPE
*Breadth across the user journey and integrations, with constrained depth in each component.*

- Guided concussion triage and recovery flow via Custom GPT
- Integration between GPT and FastAPI backend for data handling
- Encoded SCAT6-style recovery logic
- Export of structured data using FHIR format (e.g., Observation, Condition)
- Use of mock wearable data to influence recovery decisions
- Deployed system with a cloud URL for access and experimentation
- Dashboard views for sport org stakeholders (basic prototype)
- CoT and reasoning trace logging across tasks
- Git-tracked delivery flow using ai-delivery-framework tools

### 🚫 OUT OF SCOPE
*Deferred to future iterations.*

- OAuth/SMART on FHIR integration
- Live device pairing for wearables
- Real authentication and multi-user management
- Formal privacy/legal reviews
- Native mobile app deployment