# Codex Agent Task: Visit Summary HTML Parser

## 🎯 Goal
Extract structured visit summary data from HTML pages.

## 📂 Target File
- `app/processors/visit_html_parser.py`

## 📋 Instructions
- Accept an HTML string input
- Use `BeautifulSoup` to parse the HTML
- Extract fields:
  - `date`
  - `provider`
  - `doctor`
  - `notes`
- Return list of dicts (one per visit):
```json
{
  "date": "2023-06-01",
  "provider": "General Hospital",
  "doctor": "Dr. Jones",
  "notes": "Follow-up recommended."
}
```
- Add a test case using a sample HTML string with known structure

## 🔄 Reuse
- Leverage existing scraping structure and portal adapters from `app/adapters/`

## ✅ What to Report Back
- Parser function, test file, and example output
- Assumptions on HTML layout

Refer to `task_guides/review_checklist.md` for structure.