# Task 211: Structured Record Session Filter + ETL Log Cleanup

## 🎯 Goal
Support multi-user ingestion and improve ETL log readability by filtering structured records by session and reducing noisy trace logs.

---

## 🔧 Subtasks

### 🔹 Task 211.1: Add `session_key` to StructuredRecord
- Update `StructuredRecord` model:
```python
session_key = Column(String, index=True)
```
- Include this in `insert_structured_records()` and all ETL insert logic
- Ensure `/status` and `/ask` only return results scoped to that session

### 🔹 Task 211.2: SQL Migration
- Generate SQL query to DROP and recreate `structured_records` table with new `session_key` column
- Include default (`NULL`) for backward compatibility if needed

### 🔹 Task 211.3: Streamline ETL Logging
- Remove or suppress noisy `httpx`, `azure`, and `openai` logs (e.g., via `logging.getLogger('azure').setLevel(logging.WARNING)`)
- Add high-level ETL progress logs: `"Inserting X structured records for session Y"`, `"ETL complete for session Y"`
- Include blob name in summaries for easier trace

---

## 📂 Target Files
- `app/storage/models.py`
- `app/storage/structured.py`
- `app/orchestrator.py`
- `scripts/export_records.py`, `/ask` tool (if scoped)

## 🧪 Testing
- Upload file with new session key
- Run ETL, then `/status` or `/ask` — results should match session only

## ✅ Outcome
Better support for multi-user ingestion, cleaner logs, and easier test debugging.