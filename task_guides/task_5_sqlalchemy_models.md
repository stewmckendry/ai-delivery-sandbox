# Codex Agent Task: SQLAlchemy Models for Health Data

## 🎯 Goal
Define models for storing structured health data in a SQLite DB using SQLAlchemy.

## 📂 Target Files
- `app/storage/models.py`
- `app/storage/db.py`

## 📋 Instructions
- Define `LabResult` model with fields: id, test_name, value, units, date
- Define `VisitSummary` model with fields: id, provider, doctor, notes, date
- Use declarative base in `db.py` with engine + `Base.metadata.create_all()`
- Configure SQLite in-memory or file-based DB for testing

## ✅ What to Report Back
- File paths and full content
- Test script or code block to initialize DB and insert sample data
- Unit test that validates table creation and data insertion
- Output of test run (e.g., pytest or inline test)

Refer to `task_guides/review_checklist.md` for structure.