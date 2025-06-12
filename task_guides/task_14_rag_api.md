# Codex Agent Task: Retrieval-Augmented Generation (RAG) API

## 🎯 Goal
Build an API endpoint that uses structured DB content as RAG context to answer health-related user questions.

## 📂 Target File
- `app/api/rag.py`

## 📋 Instructions
- Create POST endpoint `/ask`
- Accept JSON body with `{"query": "..."}`
- Load recent lab and visit entries from SQLite DB
- Format as context blocks (e.g., bullet list of visits + labs)
- Use OpenAI API with this context + user query to produce an answer
- Return the response string to the caller

## 🧪 Test
- Add `tests/test_rag_api.py`
- Use FastAPI TestClient
- Mock DB data and OpenAI API
- Test 1–2 known Q&A outputs

## 🔄 Reuse
- DB access from `app/storage/db.py`
- Models from `app/storage/models.py`
- LLM access from Task 13

## ✅ What to Report Back
- Endpoint code, sample input/output, test file
- Logic used to assemble context for RAG

Refer to `task_guides/review_checklist.md` for structure.