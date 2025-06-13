# Task 34 Review: Summarize Structured Records for User Preview

## ✅ Summary
Implements `summarize_database_records()` to:
- Query `LabResult`, `VisitSummary`, and `StructuredRecord`
- Compile visit notes, lab metrics, and AI-generated text
- Use `summarize_blocks()` to generate a markdown summary
- Automatically write output to `logs/portal_runs/<portal>_summary.md`

## 📂 Files Updated
- `app/orchestrator.py`
- `app/prompts/summarizer.py`
- `tests/test_orchestrator.py`
- `tests/test_summarizer.py`

## 📄 Output Sample
```md
### Portal Run Summary

The patient had 2 visits and 3 lab results.

LLM summary
```

## 🧪 Tests
```bash
pytest -q
```
- ✅ Mocked OpenAI call to verify summarization logic
- ✅ Validates content and formatting
- ✅ Verifies summary file written post-ETL

## 💬 Feedback
- ✅ Summary is user-readable and includes all record types
- ✅ Adds real value post-ETL
- 🟡 Optional: include date ranges, provider stats, etc.

## 🚀 ETL pipeline now outputs end-to-end summaries suitable for user export, preview, or reporting