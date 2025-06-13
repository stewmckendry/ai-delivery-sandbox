# Task 34: Summarize Structured Records for User Preview

## 🎯 Goal
Generate a concise, user-friendly summary of all structured records stored in the database for a portal run.

## 📂 Target Files
- `app/prompts/summarizer.py` (extend)
- `scripts/dev_seed_and_preview.py` (use)

## 📋 Instructions
- Query structured records from DB (lab, visit, structured table)
- Use `summarize_blocks()` to generate an overview:
  - “The patient had 2 visits and 3 lab results. The most recent..."
- Output should be markdown-style summary
- Optional: support `--summarize` CLI flag in preview script

## 🧪 Test
- Add mocked records
- Confirm summary output structure and tone

## ✅ What to Report Back
- Summary prompt template (if new)
- Summary generation function
- Example output from `test_portal` run