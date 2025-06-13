# Task 35: Export Structured Records to JSON / Markdown / PDF

## 🎯 Goal
Allow users to export structured lab and visit data from the database into downloadable formats for external sharing or backup.

## 📂 Target Files
- `scripts/export_records.py`

## 📋 Instructions
- Query:
  - `LabResult`, `VisitSummary`, and optionally `StructuredRecord`
- Support export formats:
  - JSON (default)
  - Markdown (via markdown2)
  - PDF (optional: via reportlab or markdown-to-pdf)
- CLI options:
```bash
python scripts/export_records.py --format markdown --output visit_summary.md
```
- Format sections by type (lab, visit, structured)

## 🧪 Test
- Use sample SQLite DB
- Confirm all export formats save as expected

## ✅ What to Report Back
- Script + supported formats
- Sample exports for `test_portal` or `test_portal_b`