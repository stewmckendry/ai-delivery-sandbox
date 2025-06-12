# Codex Agent Task: PDF Parser for Lab Results

## 🎯 Goal
Extract structured lab results from a health record PDF.

## 📂 Target File
- `app/processors/lab_pdf_parser.py`

## 📋 Instructions
- Accept a PDF filepath as input
- Use `fitz` (PyMuPDF) to read the file
- Extract test name, value, units, and date if available
- Return list of dicts:
```json
{
  "test_name": "Cholesterol",
  "value": "5.8",
  "units": "mmol/L",
  "date": "2023-05-01"
}
```
- Reuse PDF logic patterns from `app/processors/pdf_parser.py` (Task 2)
- Add a unit test using a fixture PDF or mocked input

## ✅ What to Report Back
- Parser function and test file
- Sample output for 1–2 test entries
- Known limitations (layout assumptions, missing date handling)

Refer to `task_guides/review_checklist.md` for structure.