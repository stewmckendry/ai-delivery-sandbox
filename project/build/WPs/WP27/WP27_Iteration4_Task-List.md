# WP27 Iteration 4 Task List

## ✅ 1. Infrastructure Setup

- **Redis helper module:** Create utility to manage per-session section draft state.
- **Add section state writing:**  
    When `generate_section_chain` completes, push each `(section_id, raw_draft)` into Redis under `session_id`.

## 🛠️ 2. Feedback Flow: Initial Round

- **Tool:** `feedback_preprocessor`  
    Parse user dump and map comments to relevant sections.
- **Tool:** `revise_section_chain`  
    For all impacted sections:
    - Pull original draft from Redis.
    - Rewrite using `section_rewriter`.
    - Generate diff using `diff_summarizer` (LLM-based).
    - Save `(section_id, new_draft, diff)` back to Redis.

## 🔁 3. Feedback Review Loop (per section)

- **Tool:** `section_review_manager`
    - Serve revised section and diff to GPT.
    - Track which sections are remaining.
- **GPT Action:**
    - Present section + changes to user.
    - Accept revised draft or collect new feedback.

## 📤 4. Finalization Flow

- When user has approved all sections:
    - GPT calls `assemble_artifact_chain` with updated drafts.
    - `storeToDrive` writes to Google Docs and updates logs.

## 🧠 5. Patch Coordination

Patches will be delivered in this order:
1. Redis helper module
2. Patch `generate_section_chain` to write Redis
3. Patch `revise_section_chain` to use Redis, and `diff_summarizer`
4. Implement `section_review_manager` (Redis cursor, fetch next section, etc.)
5. Wire GPT action chain (API call flow) for (a), (b), (c) from plan
6. Finalization hook once all approved