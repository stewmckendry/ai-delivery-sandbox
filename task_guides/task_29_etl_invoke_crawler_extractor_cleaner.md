# Task 29: Integrate AI-Powered Modules into ETL

## 🎯 Goal
Update `run_etl_for_portal()` to invoke:
- `crawler.py` for smart traversal
- `extractor.py` for HTML classification
- `cleaner.py` for summarization + deduplication

## 📂 Files
- `app/orchestrator.py`
- Optional: update CLI runner or logs

## 📋 Instructions
- After login:
  - Use `crawler.crawl_portal()` to fetch and score up to N pages
  - For each HTML page:
    - Use `extractor.extract_relevant_content()`
    - Clean results using `cleaner.clean_blocks()`
    - Tag each chunk with source_url, type, and portal
- Print/save structured JSON for extracted + cleaned records
- Optionally: save preview to file

## 🧪 Test
- Run with `--portal test_portal`
- Check logs and output artifacts

## ✅ What to Report Back
- New ETL section calling these modules
- Sample output from fake site

Refer to Task 27 + Task 24–26 reviews.