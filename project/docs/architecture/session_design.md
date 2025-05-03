## 🧠 Session ID Design – CareerCoach MVP

### 🔑 What is a `session_id`?
A `session_id` is a unique, anonymous identifier that represents a single user’s coaching journey.
It allows the system to persist, summarize, and resume sessions — without tracking identity.

It’s conceptually similar to a Git "branch" in the ai-delivery-framework: scoped, unique, portable.

---

### 🗂 Use Cases
| Flow | Use of session_id |
|------|-------------------|
| Save Reflection | Tags reflection (career, text, timestamp) |
| Fetch Summary   | Gathers all reflections under the same session |
| Resume Session  | Custom GPT can echo back session_id |
| Share/Export    | Session ID can be used in QR or short URL |

---

### 🧾 Format Options
- `uuid4()` → Fully unique (`17c61d35-4be1-40cc-bc1a-abc7e2a5c6cd`)
- Shortcode → Human-readable (`abc-123`, `coach-dawn-4912`)
- Prefixed → Semantic (`careercoach-session-nnnn`)

---

### ✅ Design Principles
- Stateless: Not tied to identity or login
- Portable: Can be shared or passed into GPT context
- Secure: No personal data, opaque by default
- Durable: Indexed in Airtable + Notion for journaling

---

### 🛠 Where Used
- `save_reflection`
- `fetch_summary`
- MemoryManager backend
- Optional GPT responses

This session design enables personal, private career exploration while keeping the system simple and scalable.