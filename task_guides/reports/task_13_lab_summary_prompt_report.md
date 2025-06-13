# Task 13 Review: Lab Results Summarizer Prompt

## ✅ Summary
Implemented `summarize_lab_results()` using:
- `load_prompt()` to render `summarize_lab_results.yaml`
- `app.utils.llm.chat_completion()` to call LLM with user prompt
- Returns the text of the response

## 📂 Files Created
- `app/prompts/summarizer.py`
- `tests/test_summarizer.py`

## 🧪 Unit Test
- Uses `monkeypatch` to mock OpenAI API call
- Supplies 2 lab result dicts
- Verifies summary response string

## ▶️ Sample Output
```
"Summary text"
```

To run:
```bash
PYTHONPATH=. pytest -q tests/test_summarizer.py
```

## 💬 Feedback
- ✅ Simple and effective wrapper over the prompt loader
- ✅ Clean separation of templating, LLM, and input data
- 🟡 Future: allow prompt version/config overrides for testing variants

## 🔁 Next Step
Used as core building block for RAG endpoint in Task 14