# Task 14 Review: RAG API Endpoint

## ✅ Summary
Implemented `/ask` endpoint to:
- Load recent lab + visit summaries from DB
- Construct a formatted context block
- Use OpenAI API with user's question
- Return generated answer string

## 📂 Files Created
- `app/api/rag.py`
- `tests/test_rag_api.py`
- `app/api/__init__.py` updated to include new router

## ▶️ Sample Prompt Construction
```
Recent Lab Results:
- Cholesterol: 5.8 mmol/L (2023-05-01)

Recent Visits:
- 2023-06-01 - General Hospital - Dr. Jones: Routine check

Question: How am I doing?
```

## ✅ Unit Test
- Injects mock data into temp DB
- Mocks OpenAI response
- Asserts structured prompt contains key fields
- Confirms output matches expected answer

Run with:
```bash
PYTHONPATH=. pytest -q tests/test_rag_api.py
```

## 💬 Feedback
- ✅ Fully self-contained API logic
- ✅ Handles context generation and DB wiring well
- ✅ Strong test coverage including OpenAI mock and data verification
- 🟡 Could allow max results config via query param in future

## 🚀 Ready for usage as health assistant Q&A endpoint