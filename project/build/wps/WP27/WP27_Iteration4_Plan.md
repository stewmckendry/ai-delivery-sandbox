## WP27 Iteration 4 Plan – Feedback-Driven Revisions

### 🎯 Goal
Enable users to submit document-level feedback that is processed and incorporated into revised section drafts, reviewed collaboratively, and finalized into a new document version.

---

## 🧠 Roles & Responsibilities

| Actor                | Responsibility                                                                 |
|----------------------|------------------------------------------------------------------------------|
| User (via GPT chat)  | Submit feedback, review each revision, approve or refine                      |
| GPT (chat layer)     | Guide review, summarize diffs, coordinate toolchain calls                     |
| Toolchains           | Apply feedback, manage section rewriting, save versions                        |
| Redis                | Temporary in-memory store for revised sections and diffs                      |
| LLM (in tools)       | Rewrite sections and generate diff summaries                                  |

### ✍️ (Updated for Section Generation)
| Actor                | Responsibility                                                                 |
|----------------------|------------------------------------------------------------------------------|
| User (via GPT chat)  | Provide topic input / seed text for a section draft                           |
| GPT (chat layer)     | Trigger section generation, explain outputs, capture user feedback            |
| Toolchains           | Synthesize section content from memory, profile, context, etc.                 |
| Redis                | (New) Save raw_draft per section_id for review or revision path                |
| LLM (in tools)       | Compose initial draft based on structured and contextual inputs               |

---

## 🔄 End-to-End Flow

### (a) Submit Feedback
1. **User** sends feedback in any form (dump, general, or specific)
2. **GPT** calls: `revise_section_chain`
   - Tools invoked:
     - `feedback_preprocessor`: parse feedback into target section_ids + rationale
     - `memory_retrieve`: pull memory + original drafts from DB
     - `section_rewriter`: re-write all impacted sections
     - `diff_summary`: summarize LLM-generated differences from original
     - `manualEditSync`: store revised drafts to DB
   - Stores: section_id → {text, diff} in Redis
   - Logs: `DocumentFeedback`
3. **GPT** sends user a summary of affected sections, and what changed

### (b) Section-by-Section Review
1. **GPT** shows user next revised section + diff summary
2. **User** can:
   - ✅ Approve (move to next)
   - ✏️ Submit feedback → rerun `revise_section_chain` w/ new input
   - 🔁 Re-review until all confirmed
3. **Redis** updated with latest draft + diff per round

### (c) Finalization
1. After last section confirmed
2. **GPT** calls: `finalize_document_from_revisions`
   - Pulls section drafts from Redis
   - Triggers `assemble_artifact_chain`
   - Pushes to Drive via `storeToDrive`
   - Logs `DocumentVersionLog`
   - Sends doc link to user


---

## 🔌 Redis Schema
```
Key: revision:<session_id>:<section_id>
{
  "section_id": "background",
  "text": "...",
  "diff_summary": "Added details on..."
}
```

Also consider `revision:<session_id>:section_order` to manage review flow

---

## 🔧 Toolchain Enhancements

### ✅ PATCH 1: Redis Storage in generate_section_chain
- **Why**: unify flows and allow revise flow to re-use previous section drafts
- **Where**: end of `generate_section_chain`, after section_synthesizer
- **How**: add Redis client write: 
```python
redis_key = f"revision:{session_id}:{section_id}"
redis_client.set(redis_key, json.dumps({
  "section_id": section_id,
  "text": draft["raw_draft"]
}))
```

### ✅ PATCH 2: Add citations prompt support (completed)
- Applied to `summarize_global_context`, `section_synthesizer`, `refinement`
- Uses MLA-style in-text citation formatting

---

## 📦 API Tools (GPT Invokes)

### Submit Feedback (All at Once)
`POST /toolchains/revise_section_chain`
- input: { feedback, project_id, session_id, artifact_id, gate_id }
- output: { summary of revisions + Redis keys to fetch sections }

### Review Revised Section (Per Section)
`POST /tools/fetch_revision_section`
- input: { section_id, session_id }
- output: { text, diff_summary }

### Submit Section Feedback (Per Section)
`POST /toolchains/revise_section_chain`
- input: { section_id, feedback }

### Finalize
`POST /toolchains/finalize_document_from_revisions`
- Assembles revised sections into a new doc

---

## ✅ Changelog Update
- Expanded responsibilities to include generate_section_chain
- Confirmed Redis integration
- Shared finalization logic
- Committed as: `project/build/wps/WP27/WP27_Iteration4_Plan.md`

---

## ✅ Next Steps
1. Implement Redis write in `generate_section_chain`
2. Build and test `finalize_document_from_revisions`
3. Wire up new toolchain tool entries for GPT
4. Validate review loop timing
5. Pilot with feedback injection across multiple sections
