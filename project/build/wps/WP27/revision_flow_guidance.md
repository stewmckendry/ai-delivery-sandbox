## Feedback Processing vs. Section Review Flow: When to Call Which Tool

This guidance clarifies when the custom GPT should invoke `revise_section_chain` vs. `section_review_feedback`, to ensure appropriate flow and responsibility across the document revision lifecycle.

---

### 🛠️ `revise_section_chain`

**Purpose:** Bulk feedback ingestion and revision across multiple sections.

**Use when:**
- User submits **initial or general feedback** (often unstructured).
- Feedback applies to multiple sections or the full artifact.
- User is **not yet reviewing section-by-section**.

**Flow:**
1. Feedback is preprocessed and mapped to sections.
2. Each impacted section is revised.
3. A diff summary is generated.
4. The new section and diff are saved in Redis.
5. GPT returns a high-level summary of changes.

**Called by:** GPT when user submits bulk feedback.

---

### 🧠 `section_review_feedback`

**Purpose:** Apply feedback **during interactive review** of individual revised sections.

**Use when:**
- User is **reviewing sections one by one** (post `revise_section_chain`).
- User comments on a revised section: e.g., "Can you clarify this point?"
- Feedback applies to **one specific section** currently under review.

**Flow:**
1. Feedback is applied to the given section.
2. Section is revised.
3. New diff is generated.
4. Redis entry is updated.

**Called by:** GPT during section-by-section review.

---

### 🔄 Full Flow Summary

| Step | Action | Tool/Flow | Called By |
|------|--------|-----------|-----------|
| 1 | User submits feedback (bulk) | `revise_section_chain` | GPT |
| 2 | GPT shows revision summary + changes saved to Redis | GPT | GPT |
| 3 | User begins reviewing sections | Redis → GPT | GPT |
| 4 | User provides feedback on a revised section | `section_review_feedback` | GPT |
| 5 | GPT revises section and updates Redis | GPT | GPT |

---

### 🧭 Notes for GPT Prompt Logic

- Ask user: “Would you like to submit overall feedback or review individual sections?”
- Use `revise_section_chain` for first case; enter section review mode for second.
- Store `in_review_mode=True` in GPT memory once review starts.
- For each review step:
  - Fetch section text + diff from Redis.
  - Present to user.
  - Accept feedback and call `section_review_feedback` if needed.

This separation ensures scalable feedback processing and high-integrity section-by-section revision, aligned with user intent.
