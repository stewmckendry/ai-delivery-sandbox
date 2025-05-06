## 🧪 Test Package 01 – Explorer Flow via CareerCoach-GPT

### 🎯 Goal
Simulate a full Explorer user session using the CareerCoach-GPT, from journaling to reflection saving and summary retrieval. This test validates that the GPT experience handles prompts, segment matching, and memory interactions as expected.

---

### 🧒 Scenario: Dream Job Journey

**Setup**:
- Session ID: `test_explorer_001`
- Prompt ID: `dream_job`
- Category: `creative`
- Career ID to use (optional): `creative_designer`

**Steps**:
1. GPT is prompted with: “Can you help me dream up a cool future job?”
2. GPT loads prompt via `load_prompt?prompt_id=dream_job`
3. GPT walks the user through the questions (5 expected)
4. User answers at least 3 questions (100+ chars combined)
5. GPT suggests a career (via `get_yaml_segment?category=creative`)
6. GPT prompts the user to reflect
7. GPT captures reflection and calls `record_reflection` with:
    - session_id: `test_explorer_001`
    - prompt_id: `dream_job`
    - career_id: `creative_designer`
    - text: [user reflection]
8. GPT is prompted: “Can I see what I said earlier?”
9. GPT calls `fetch_summary?session_id=test_explorer_001`

---

### ✅ Success Criteria
- Prompt questions are shown in chat
- Career card is relevant and specific
- Reflection is saved (confirm in Notion and Airtable)
- Summary returns reflection text and career insights

---

### 🧠 Post-Test Review
- **In Notion**: Look for a new entry with the prompt ID, reflection text, and session ID
- **In Airtable**: Check that a new row appears for session `test_explorer_001`, tagged with `dream_job`, category `creative`, and includes full reflection text

---

### ⏭️ Next Steps
Once this test is confirmed, repeat with a second category (e.g. `stem`) to check variability and flow reuse.