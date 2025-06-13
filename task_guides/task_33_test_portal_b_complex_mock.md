# Task 33: Create test_portal_b Adapter with Complex Content

## 🎯 Goal
Simulate a more realistic healthcare portal with:
- Multi-page structure
- Mixed content types and layouts
- Modal, table, or tab-based presentation

## 📂 Target File
- `app/adapters/test_portal_b.py`

## 📋 Instructions
- Extend from test_portal but:
  - Add 3+ pages (linked via nav)
  - Visit summary in modal (HTML)
  - Lab result in table (PDF or HTML)
  - Downloadable link to billing summary (TXT or PDF)
- Return file paths for all artifacts to orchestrator
- Ensure `/tmp/` cleanup or overwrite safety

## 🧪 Test
```bash
python scripts/run_portal_test.py --portal test_portal_b --debug
```
- Confirm log output, audit entries, and file summary

## ✅ What to Report Back
- Adapter file
- Screenshots if needed
- Summary log for new test case

This will validate system robustness against more realistic portal layouts.