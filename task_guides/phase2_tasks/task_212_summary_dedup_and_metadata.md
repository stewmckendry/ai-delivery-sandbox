# Task 212: Enhance Summary Filtering, Deduplication, and Metadata

## 🎯 Goal
Improve `/summary` UX for multi-user environments and enable smarter handling of repeated uploads or overlapping record content.

---

## 🧩 Subtasks

### 🔹 Task 212.1: Filter /summary by `session_key`
- Modify query to scope uploads, records, and summaries to the provided session only
- Avoid listing data from other sessions or system-level content

### 🔹 Task 212.2: Deduplication Heuristic (Same File Re-upload)
- On insert to `structured_records`, skip or mark duplicates
  - Detect matching: same `text`, `source_url`, and `session_key`
- Alternatively, add `is_duplicate` flag
- Optional: add `version` field per session + file

### 🔹 Task 212.3: Metadata Enrichment
- Capture and surface in `/summary`:
  - `filename`, `portal`, `timestamp`
  - Source path (e.g. blob name)
  - Insert time and any duplication flags
- Show most recent record date per type (labs, visits, activities)

### 🔹 Task 212.4: LLM-based Redundancy Detection (Optional)
- On batch insert: batch structured records and query LLM for semantic overlap
- Log if multiple records are essentially “near duplicates”
- Store result in `user_notes` or a new `llm_annotation` field

---

## 📂 Target Files
- `app/api/status.py`
- `app/storage/models.py`, `structured.py`
- `app/orchestrator.py`
- `project/docs/operator_guidance.md`

## 🧪 Testing
- Upload same file multiple times
- Confirm `/summary` reports a single upload record or flags duplicates
- Ask tool output should remain consistent with latest data

---

## ✅ Outcome
Cleaner summaries, smarter deduplication, and richer user feedback. Paves the way for LLM-assisted record validation and summarization.