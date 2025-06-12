# Task 28 Review: ETL Test Script + Integration Validation

## ✅ Summary
Implements a CLI tool `run_portal_test.py` to:
- Run the full `run_etl_for_portal()` pipeline
- Capture start/end time, status, and runtime artifacts
- Save JSON logs to `logs/portal_runs/`
- Test using a fake `test_portal` adapter with generated HTML + PDF

## 📂 Files
- `scripts/run_portal_test.py`
- `app/adapters/test_portal.py` (implicit)

## ▶️ Usage
```bash
python scripts/run_portal_test.py --portal test_portal --depth 2 --debug
```

## 🧪 Behavior
- Loads scraper and credentials
- Runs scraper and challenge logic if needed
- Extracts + classifies content
- Summarizes and deduplicates output
- Stores files and DB entries
- Writes final summary to timestamped JSON file

## 🧾 Sample Log Output
```json
{
  "portal": "test_portal",
  "depth": 2,
  "start_time": "2025-06-12T19:53:39.461896",
  "success": true,
  "duration_seconds": 0.427
}
```

## 💬 Feedback
- ✅ Script is portable, debug-friendly, and log-rich
- ✅ Supports test and real portal runs
- ✅ Screenshot artifact collection supports future CI review
- 🟡 Future: include structured output preview in the summary

## 🚀 Ready to use for all pipeline validation and QA runs