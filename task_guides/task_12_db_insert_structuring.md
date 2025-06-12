# Codex Agent Task: Structuring and DB Insert Logic

## 🎯 Goal
Take cleaned structured data and save to the SQLAlchemy database.

## 📂 Target File
- `app/processors/structuring.py`

## 📋 Instructions
Implement:
```python
def insert_lab_results(session, results: list[dict]):
    # converts list of dicts to LabResult objects and saves

def insert_visit_summaries(session, summaries: list[dict]):
    # same for VisitSummary
```
- Use SQLAlchemy models from `app/storage/models.py`
- Accept a session from `app/storage/db.py`
- Add a test with an in-memory SQLite DB to validate insert and retrieval

## 🔄 Reuse
- Models from `app/storage/models.py`
- DB setup from `app/storage/db.py`
- Example outputs from tasks 10 + 11

## ✅ What to Report Back
- Implementation and test file
- Sample test data and console output
- Notes on edge cases (e.g., duplicate entries)

Refer to `task_guides/review_checklist.md` for structure.