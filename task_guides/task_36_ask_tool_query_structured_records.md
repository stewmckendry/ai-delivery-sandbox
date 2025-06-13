# Task 36: Implement ASK Tool to Query Structured Records

## 🎯 Goal
Allow users to ask natural-language questions (via CLI or ChatGPT) and receive answers based on structured records stored from the ETL pipeline.

## 📂 Target File
- `scripts/ask_tool.py` (new)
- May reuse: `app/api/rag.py` logic

## 📋 Instructions
- CLI usage:
```bash
python scripts/ask_tool.py --query "What were my last lab results?"
```
- Load structured records from DB:
  - `LabResult`, `VisitSummary`, `StructuredRecord`
- Format as context (JSON or bullet list)
- Send context + query to OpenAI llm.py
- Print the answer to stdout

## 🧪 Test
- Use sample DB content or fixture loader
- Run with query and validate returned answer

## ✅ What to Report Back
- CLI tool implementation
- Sample query + answer
- Output context size or metadata

This tool complements export + summarization features, giving users conversational access to their data.