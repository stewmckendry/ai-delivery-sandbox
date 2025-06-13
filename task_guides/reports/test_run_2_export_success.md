# 📄 Test Run 2 (Export Phase) – test_portal_b

## 🧪 Command Summary
```bash
python scripts/export_records.py --format markdown --output test_portal_b_export.md
python scripts/export_records.py --format pdf --output test_portal_b_export.pdf
python scripts/export_records.py --format json --output test_portal_b_export.json
```

## 📦 Output Files
- `test_portal_b_export.md`
- `test_portal_b_export.pdf`
- `test_portal_b_export.json`

## ✅ Export Stats
- Labs: 2
- Visits: 1
- Structured Records: 10

## 🔍 Export Snippet (Markdown)
```markdown
## Lab Results
- 2023-05-01 Cholesterol 5.8 mmol/L
- 2023-05-02 Hemoglobin 13.5 g/dL

## Visit Summaries
- 2023-06-01 General Hospital Dr. Jones: Routine check

## Structured Records
- [lab_result] Lab Results (/tmp/test_b_dash_4c099dec.html)
- [visit_note] Visits (/tmp/test_b_dash_4c099dec.html)
...
```

## 💃 Record Highlights
- Billing info: `$100 due by July 1, 2023`
- Visit note: `Routine check on June 1, 2023`
- Labs: `Cholesterol 5.8`, `Hemoglobin 13.5`

## 💬 Feedback
- ✅ Clean structure and export coverage
- 🔹 Consider PDF styling enhancements (headers, spacing)

## 🚀 Export phase complete. Moving to ASK tool testing next.