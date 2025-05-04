## 🧩 CareerCoach MVP – Technical Design Specs

---

### 1. 🎛 Prompt Selector UI

**Endpoint:** `/load_prompt`  
**Defined in:** `routes/prompts.py`, `utils/prompt_loader.py`

**Input:** `prompt_id` (query param, string)  
**Output:** JSON coaching prompt structure

**GPT Tool Contract:** Matches OpenAPI `/load_prompt` (GET) in `fastapi_and_gpt_scaffolds.md`

**Edge Cases:**
- Invalid `prompt_id` → 404 with fallback message
- Network error → GPT should say: "Hmm, couldn't load that journey. Want to pick another?"

**Testing Notes:**
- Validate JSON structure per prompt
- Simulate missing/invalid prompt ID

---

### 2. 🤖 Guided Q&A Flow

**GPT Behavior:**
- Driven by loaded prompt sequence (internal logic)
- No backend call needed per question

**GPT Tool Contract:** Only for `/load_prompt` and `/save_reflection`

**Edge Cases:**
- Misinterpreted input → GPT retries question
- User stops midway → session remains open

**Testing Notes:**
- Validate prompt coverage (3+ Qs per path)
- Age-appropriate tone and readability

---

### 3. 🃏 Career Card Generator

**GPT Behavior:**
- Uses `/get_yaml_segment` to fetch relevant segment

**Endpoint:** `/get_yaml_segment`  
**Defined in:** `routes/segments.py`, `utils/yaml_loader.py`

**Input:** `category` (query param, string)  
**Output:** JSON array of careers

**GPT Tool Contract:** Matches OpenAPI `/get_yaml_segment` (GET) in `fastapi_and_gpt_scaffolds.md`

**Edge Cases:**
- Invalid category → 404 with fallback logic
- No match found → GPT defaults to "Want to try a new direction?"

**Testing Notes:**
- YAML schema integrity
- Validate one match is returned with all fields

---

### 4. 📝 Journaling / Reflection

**Endpoint:** `/save_reflection`  
**Defined in:** `routes/memory.py`, `utils/memory_manager.py`

**Input:** JSON `{session_id, career_id, prompt_id, text}`  
**Output:** `{ success: boolean }`

**GPT Tool Contract:** Matches OpenAPI `/save_reflection` (POST) in `fastapi_and_gpt_scaffolds.md`

**Edge Cases:**
- Network/memory error → GPT responds with retry invite
- Text < 100 chars → GPT nudges user to reflect more

**Testing Notes:**
- Test both Airtable and Notion pathways
- Validate payload fields are persisted

---

### 5. 🔁 Try Another Path

**GPT Behavior:**
- Re-initiates prompt selector logic
- Can reuse session ID

**Edge Cases:**
- Repeat prompt → ensure variety or nudge

**Testing Notes:**
- Session continuity
- Prompt reset logic cleanly reloads state

---

### 6. 📌 Favorites Shelf

**Storage:** Frontend local/session storage  
**Backend involvement:** None — not in scaffold

**Edge Cases:**
- Max 3+ entries
- Browser refresh resets unless session saved externally

**Testing Notes:**
- UI behavior on add/remove
- Storage lifespan (until tab close)

---

### 7. 💾 Backend Memory (Optional)

**Covered via:** `/save_reflection`, `/fetch_summary`  
**Defined in:** `routes/memory.py`, `utils/memory_manager.py`

**Endpoint:** `/fetch_summary`  
**Input:** `session_id`  
**Output:** `{ summary: string }`

**GPT Tool Contract:** Matches OpenAPI `/fetch_summary` (GET) in `fastapi_and_gpt_scaffolds.md`

**Edge Cases:**
- Empty session → GPT fallback message
- Large sessions → truncate/format gracefully

**Testing Notes:**
- Summary output from both Notion/Airtable
- Validate consistency of ID use

---

### 8. 📚 RAG Knowledgebook (Optional)

**Source:** YAML segments per category from GitHub  
**Loader defined in:** `utils/yaml_loader.py`

**Edge Cases:**
- Schema drift → validate fields (emoji, traits, path)

**Testing Notes:**
- Field presence and formatting
- Source tag citations in GPT response

---

### 9. 🧑‍🏫 Group Mode (Experimental) — *Deferred post-MVP*

**Behavior:**
- Prompt launched across multiple devices via shared link or QR code
- Reflections optionally aggregated

**Requirements:**
- Route or method to batch-fetch reflections by `group_id` or tag

**Edge Cases:**
- Mixed session times → sync guidance
- Shared devices → avoid ID collisions

**Testing Notes:**
- Test QR generation, joining via shared link, and group summaries

---

### 10. 🧠 Profile Summary View (Experimental) — *Deferred post-MVP*

**Behavior:**
- User sees a summarizing "You are..." card based on their inputs

**Source:**
- GPT synthesizes from all reflections in session

**Edge Cases:**
- Insufficient input → GPT offers invitation to explore more

**Testing Notes:**
- Summary coherence, personalization
- Optional template consistency

---

All routes conform to FastAPI standards. GPT tool contracts align with OpenAPI schema in `fastapi_and_gpt_scaffolds.md`. MemoryManager supports dual-write logic and can be mocked for test automation.

Next step: Implementation begins with FastAPI routes, YAML loaders, and memory handlers for MVP endpoints.