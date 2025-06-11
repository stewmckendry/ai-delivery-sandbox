# Codex Agent Task: PDF Parsing with PyMuPDF (Spike)

## 🎯 Goal
Create a PDF parser that extracts lab results and returns them as structured data.

## 📂 Target File
`app/processors/pdf_parser.py`

## 📋 Instructions
- Use `fitz` from PyMuPDF to open and read the PDF
- Extract text while preserving layout if possible
- Identify and extract lab results with fields like:
  - test name
  - result value
  - units
- Return the data as a list of dictionaries

## ✅ What to Report Back
- File path and function code
- Example input/output
- CLI/test command to verify output
- Edge cases or limitations
- Any formatting assumptions

Refer to [review_checklist.md](review_checklist.md) for formatting.