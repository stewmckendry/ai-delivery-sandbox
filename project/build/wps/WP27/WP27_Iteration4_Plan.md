## 🧹 Iteration 4 Plan: Feedback Review & Section Rewriting Flow

### 🌟 Objectives
- Allow users to submit feedback and receive revised sections.
- GPT iteratively presents each revision for approval or further edits.
- Once all confirmed, the final document is reassembled and delivered.

---

### 🧐 Roles
| Actor | Responsibility |
|-------|----------------|
| User (via GPT chat) | Submit feedback, review each revision, approve or refine |
| GPT (chat layer) | Guide review, summarize diffs, coordinate toolchain calls |
| Toolchains | Apply feedback, manage section rewriting, save versions |
| Redis | Temporary in-memory store for revised sections and diffs |
| LLM (in tools) | Rewrite sections and generate diff summaries |

---

### 🔁 E2E Flow

#### (a) Initial Feedback Submission (multi-section)
1. **User** provides general or specific feedback via GPT.
2. **GPT** calls toolchain: `submit_feedback_batch`:
   - Maps feedback to impacted sections
   - Rewrites all impacted sections (via `section_rewriter`)
   - Generates `diff_summary` via LLM per section
   - Stores `section_id`, `raw_draft`, `diff_summary` in Redis
   - Returns revision summary + count to GPT

#### (b) Section-by-Section Review
1. **GPT** fetches next from Redis:
   - Calls: `get_next_section_for_review`
   - Returns: `section_id`, `draft`, `diff_summary`, `remaining_count`
2. **User** approves or refines

#### (c) Per-Section Revision Feedback
1. **User** submits new feedback for a section
2. **GPT** calls toolchain: `submit_feedback_for_section`
   - Rewrites impacted sections again
   - Updates Redis with new drafts + diff_summaries
   - Returns update summary to GPT

#### (d) Finalization
1. After last section confirmed
2. **GPT** calls: `finalize_document_from_revisions`
   - Pulls current drafts from Redis
   - Triggers `assemble_artifact_chain`
   - Pushes to Drive via `storeToDrive`
   - Logs `DocumentVersionLog`
   - Sends doc link to user

---

### 🔧 Patch Plan

#### Phase 1: Core Toolchain Updates
- [ ] Update `revise_section_chain.py`:
  - Return list of revised sections + diff_summary
  - Write to Redis with TTL keyed by session_id + section_id
- [ ] Add LLM-powered `diff_summary` prompt tool

#### Phase 2: GPT Interaction APIs
- [ ] Tool: `submit_feedback_batch`
- [ ] Tool: `get_next_section_for_review`
- [ ] Tool: `submit_feedback_for_section`
- [ ] Tool: `finalize_document_from_revisions`

---

### 📍 Redis Plan
- Reuse existing Redis infra
- Use key schema:
  - `revise:{session_id}:{section_id}` → JSON blob with `draft`, `diff_summary`
  - `revise:queue:{session_id}` → list of section_ids to track queue

---

### 📌 Prompt Additions
- `revision_prompts.yaml`
  - `diff_summary`:
    - System: "You summarize edits to policy drafts."
    - User: Provide original + revised → explain what changed and why

---

### 📦 Commit Info
- Repo: `ai-delivery-sandbox`
- Branch: `sandbox-curious-falcon`
- Task: `WP27`