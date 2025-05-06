## 🗃️ Data Store Explainer – Notion & Airtable in CareerCoach

This doc explains how Notion and Airtable are used as backend stores in the CareerCoach MVP. Though not visible to end-users, they power journaling and insight generation.

---

### 📚 1. Purpose of Using Notion and Airtable

| Goal | Store | Reason |
|------|-------|--------|
| Store rich reflections | Notion | Structured, readable journaling log |
| Track prompt+session metadata | Airtable | Easier API access, tabular indexing |
| Enable admin insight tools | Both | Notion for review, Airtable for analytics |

---

### 📝 2. What Gets Stored

#### 🔐 Notion
- Reflection text per journaling session
- Prompt ID used
- Optional: Career category or segment match
- Timestamp

#### 📊 Airtable
- session_id
- prompt_id
- user text
- category (if detected)
- structured timestamp

---

### 👥 3. Users and Access

| Role | Access | Use |
|------|--------|-----|
| End-user | ❌ No direct access | They interact only through GPT/journaling UX |
| Mentor/Coach | ✅ Notion only | Review logs, spot trends |
| Product Owner | ✅ Both | Review data, test improvements |
| Dev/Infra | ✅ Both | Debug, schema alignment, testing |

---

### 🔁 4. Data Flow Overview

1. GPT collects journal answers from the user
2. GPT posts reflection to `/record_reflection`
3. Backend stores the data to:
   - Notion (for rich text journaling)
   - Airtable (for indexing/queries)
4. Admins or mentors view logs via Notion (manual or automated)
5. Product team runs analysis from Airtable

---

This dual-store setup balances human-readability (Notion) with lightweight analytics (Airtable), while keeping all end-user logic GPT-facing.