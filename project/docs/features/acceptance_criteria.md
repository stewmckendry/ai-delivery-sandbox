## ✅ MVP Acceptance Criteria – AI Career Coach

### 🎯 1. Prompt Selector UI
- Users can view and select from at least 3 predefined prompts
- Each prompt launches a corresponding guided Q&A session
- Users may also optionally type their own open-ended question to trigger the GPT coach
- Mobile and tablet views are clean and accessible

---

### 🧠 2. Guided Q&A Flow
- Each Q&A flow includes at least 3 interactive questions
- User selections are stored in-session and influence GPT output
- All questions use kid-appropriate tone and reading level

---

### 💡 3. Career Card Generator
- GPT returns a career name, emoji, 1–2 sentence summary, and 2+ supporting traits/skills
- Results vary based on user responses
- Career card is styled visually and readable on small devices

---

### 📝 4. Journaling / Reflection
- Users can enter at least 100 characters of freeform reflection
- Reflection is stored locally and linked to the generated career
- Optional: Users can review or export all reflections

---

### 🔁 5. Try Another Path
- Users can restart with a new prompt without page reload
- Flow does not lose previously saved results

---

### 📌 6. Favorites Shelf
- User can save 3+ careers during a session
- Saved careers are viewable in a dedicated “favorites” view
- Data persists until browser tab closes or user resets

---

### 💾 7. Backend Memory (Optional)
- User reflections and career selections can be written to Airtable or Notion
- Data is linked to a user ID/session ID without storing identity
- GDPR-style note: no PII collected; everything opt-in

---

### 🧠 8. RAG Knowledgebook (Optional)
- GPT uses grounding data from custom RAG store for career lookups
- Responses cite source tags (e.g. [from RAG: Exploratorium Guide])
- No direct internet search or open web used