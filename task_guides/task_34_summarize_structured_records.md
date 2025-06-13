# Task 34: Summarize Structured Records for User Preview

## 🎯 Goal
Generate a concise, user-friendly summary of all structured records stored in the database for a portal run.

## 📂 Target Files
- `app/prompts/summarizer.py` (extend)
- `app/orchestrator.py` (optional wiring)

## 📋 Instructions
- Query structured records from DB (lab, visit, structured table)
- Use `summarize_blocks()` to generate an overview:
  - “The patient had 2 visits and 3 lab results. The most recent..."
- Output should be markdown-style summary

### Optional (recommended)
- Call this at the end of `run_etl_for_portal()`
- Log summary to console or write to file:
```python
summary = summarize_blocks([{"text": r["text"]} for r in final_records])
with open(f"logs/portal_runs/{portal}_summary.md", "w") as f:
    f.write(summary)
```

## 🧪 Test
- Add mocked records
- Confirm summary output structure and tone

## ✅ What to Report Back
- Summary prompt template (if new)
- Summary generation function
- Example output from `test_portal` run

This enables quick understanding of ETL outcomes for devs or end users.