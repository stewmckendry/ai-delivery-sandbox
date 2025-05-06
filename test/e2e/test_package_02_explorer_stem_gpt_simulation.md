## 🧪 Test Package 02 – Explorer STEM Journey via CareerCoach-GPT

### 🎯 Goal
Simulate a STEM-focused Explorer flow using CareerCoach-GPT — validate the journaling, segment fetch, and memory tools, and practice extracting value from the saved data in Notion and Airtable.

---

### 🧒 Scenario: Problem Solver in STEM

**Setup**:
- Session ID: `test_explorer_002`
- Prompt ID: `problem_solver`
- Category: `stem`
- Career ID (suggested): `stem_inventor`

**Steps**:
1. GPT is prompted: “I want to help the world with science!”
2. GPT loads prompt via `load_prompt?prompt_id=problem_solver`
3. GPT guides the user through 5 questions
4. User answers at least 3 (100+ chars total)
5. GPT loads STEM careers via `get_yaml_segment?category=stem`
6. GPT suggests a STEM job (e.g., Inventor, Scientist)
7. GPT captures reflection and calls `record_reflection` with:
    - session_id: `test_explorer_002`
    - prompt_id: `problem_solver`
    - career_id: `stem_inventor`
    - text: [user reflection]
8. GPT is prompted: “Can you remind me what I wrote?”
9. GPT calls `fetch_summary?session_id=test_explorer_002`

---

### ✅ Success Criteria
- STEM career is relevant and rooted in user’s problem area
- Reflection saved and summary retrieved
- `career_id` is included correctly in the memory save

---

### 🧠 Post-Test Review Instructions

#### 🔍 In **Notion**:
- Open the Notion log tied to CareerCoach (you may have a shared table or workspace)
- Filter or search by `session_id = test_explorer_002`
- Confirm reflection text appears with prompt title and timestamp
- Copy or clip text to use in coaching conversations

#### 📊 In **Airtable**:
- Open the CareerCoach Airtable base
- Filter by `session_id = test_explorer_002`
- Add a filter for `category = stem`
- Look for columns: prompt_id, career_id, text
- Try: grouping by prompt_id or charting reflection lengths for STEM

**New to Airtable?** Try these first:
- Click "Group" and group by `prompt_id` to see what themes are popular
- Click "Filter" to isolate reflections by category or keywords
- Click "Apps" > "Charts" (if enabled) to graph categories or reflection lengths

---

### 🔁 Suggested Variations
- Run again with prompt `curiosity_lab` or `inventors_workshop`
- Use different categories (e.g. `earth`, `people`, `creative`)

---

**Status**: ✅ Ready for manual execution. Confirm reflection saves and analyze in Notion/Airtable.