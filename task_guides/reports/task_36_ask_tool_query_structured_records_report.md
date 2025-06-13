# Task 36 Review: ASK Tool to Query Structured Records

## ✅ Summary
Implements `scripts/ask_tool.py`, a CLI that:
- Loads recent records from `LabResult`, `VisitSummary`, and `StructuredRecord`
- Formats content into bullet-point context
- Sends context + query to LLM using `chat_completion`
- Prints response and metadata

## 🧪 Sample Usage
```bash
python scripts/ask_tool.py --query "What were my recent lab results?"
```

## 📂 Files
- `scripts/ask_tool.py`
- `tests/test_ask_tool.py`

## ✅ Features
- Loads from local SQLite database (custom path via `--db`)
- Returns answer from LLM (mocked in test)
- Reports counts of records used in context

## 🧪 Tests
```bash
pytest -q tests/test_ask_tool.py
```
- ✅ Injects lab, visit, structured records
- ✅ Verifies LLM context formatting and response
- ✅ Reloads DB modules after test to avoid state bleed

## 💬 Feedback
- ✅ Clean CLI interface and DB-safe
- ✅ Good example of full-stack RAG loop
- 🟡 Optionally stream or paginate context

## 🚀 This completes the ask > retrieve > answer flow using AI-native summaries.