# 🧠 Design Note: Redis as In-Memory Store for Section Edits

## Overview
This document explains the rationale for using Redis as a temporary, in-memory store for section drafts and edits during collaborative document generation workflows. It supports workflows where a user and GPT collaborate to review, refine, and finalize sections of a policy artifact.

---

## Problem
The current architecture uses a SQL database (via the `ArtifactSection` table) to persist finalized section drafts. However, during feedback and revision phases:
- Users may want to iterate on a section multiple times before committing.
- Each intermediate draft does not need to be persisted long-term.
- Rewrites and diffs must be held temporarily to support per-section review loops.

Persisting each of these to the database causes:
- Versioning bloat
- User confusion between "saved" and "in-review" versions
- Loss of agility for real-time LLM-human iteration

---

## Design Decision: Use Redis
We use Redis to store **review-phase state** for each section.
This state includes:
- `section_id`
- `raw_draft`: the revised section text
- `diff_summary`: what changed from prior version

### Redis Key Format
We use the key pattern:
```
section_review:<project_id>:<artifact_id>:<session_id>:<section_id>
```

### Redis Value Format (JSON)
```json
{
  "section_id": "problem_statement",
  "raw_draft": "...",
  "diff_summary": "Clarified language, added metrics."
}
```

---

## Benefits
✅ **Separation of concerns**: In-review vs. committed versions are kept distinct
✅ **Real-time UX**: GPT can load, revise, and present changes without touching DB
✅ **Lightweight storage**: Redis is ideal for short-lived, frequently accessed data
✅ **Simplified rollback**: User can abandon edits without affecting DB history

---

## Real-World Analogs
This pattern mirrors real-world collaborative editing systems:
- Google Docs: edits are local until saved or submitted
- GitHub PRs: branches hold proposed changes separate from `main`
- CMS draft workflows: staged drafts before publication

---

## Future Extensions
- Add TTL (time-to-live) to Redis keys to auto-expire stale sessions
- Use Redis Streams or PubSub to push updated sections to frontends
- Add version labels in Redis to allow undo

---

## Conclusion
This approach allows GPT + User collaboration with high responsiveness and low risk. It balances rapid iteration with clear finalization boundaries.

Redis is not a replacement for the database—it complements it by optimizing the **in-review experience**.