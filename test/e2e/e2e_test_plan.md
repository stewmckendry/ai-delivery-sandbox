## ✅ E2E Test Plan – CareerCoach-GPT MVP

### 🎯 Objective
Simulate real user interactions through the **CareerCoach-GPT** interface to validate Explorer and Mentor (Supporter) journeys end-to-end. All tests must be conducted through GPT tool usage — **no direct API calls**.

---

### 👧 Scenario 1: Explorer – Dream Job Journey
**Goal**: Simulate a journaling + reflection loop starting from a structured prompt.

**Steps**:
1. User says: "Can you help me dream up a cool future job?"
2. GPT selects and calls `load_prompt?prompt_id=dream_job`
3. User answers at least 3 questions (total 100+ chars)
4. GPT summarizes answers and suggests a career (calls `get_yaml_segment?category=creative` or relevant)
5. GPT prompts for reflection, receives answer
6. GPT calls `record_reflection` with session ID, prompt, and text
7. User says: "Can I see what I said earlier?"
8. GPT calls `fetch_summary?session_id=...`

**Expected**:
- Prompt and questions appear in GPT chat
- Career card is personalized and relevant
- Reflection is saved and visible via summary

---

### 👩‍👧 Scenario 2: Mentor – Review and Extend
**Goal**: Simulate a parent viewing a child’s summary and continuing the conversation.

**Steps**:
1. GPT receives parent prompt: "My child used this — what did they say?"
2. GPT calls `fetch_summary?session_id=abc123`
3. GPT summarizes the career and reflections
4. GPT offers new prompt options: “Want to try designing another job together?”

**Expected**:
- GPT returns engaging summary using previous data
- Suggested next steps build from prior answers

---

### 🧠 Notion + Airtable Usage
**Notion**:
- Mentors can browse journaling logs for each session
- Reflections include prompt, career, and full text
- Useful for qualitative insights or mentor review

**Airtable**:
- Use filters to track prompt_id usage, categories, reflection length
- Generate weekly stats: e.g., most chosen career themes
- Cross-link sessions by user ID or tag (no PII)

Example Airtable queries:
- "Show all reflections tagged 'STEM' over 200 chars"
- "Count of sessions per prompt_id"

---

### 🔍 Validation Tips
- Use a shared session_id for grouped flows
- Test saving, fetching, and resuming across sessions
- Confirm GPT reflects real-time data stored in Notion/Airtable

---

This test plan ensures validation is GPT-centered, mimics real users, and highlights downstream utility in data tools for mentors, analysts, and admins.