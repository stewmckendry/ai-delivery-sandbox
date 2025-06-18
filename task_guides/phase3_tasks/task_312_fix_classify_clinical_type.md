# 🛠️ Task 312: Fix `_classify_clinical_type` for Robust LLM Output Parsing

## 🎯 Goal
Make the LLM-based clinical classification logic resilient to invalid or malformed JSON returned by the model.

---

## 🔍 Current Issue
The `_classify_clinical_type(text)` function fails when the LLM returns improperly formatted responses such as:
- Markdown or code block wrappers
- Single-quoted JSON
- Trailing commas
- Text instead of a JSON object

This causes ETL to log:
```
LLM clinical classification failed: Expecting value: line 1 column 1 (char 0)
```

---

## ✅ What to Do
1. Update `_classify_clinical_type()` in `orchestrator.py` to:
   - Validate LLM response is **strict JSON**
   - Use `try/except` block around `json.loads(...)`
   - If parsing fails:
     - Log a warning
     - Return `None` so regex fallback can proceed

2. Optionally:
   - Clean up known LLM formatting issues (e.g., strip backticks or "json:" prefix)
   - Consider calling `chat_completion(..., functions=...)` to enforce structure

---

## 🧪 Test
- Add unit test for malformed responses (e.g., markdown-wrapped, single-quoted)
- Confirm fallback to regex still works

---

## ✅ Done When
- ETL no longer fails on LLM JSON parsing errors
- Logs show clean fallback
- Unit tests validate behavior for malformed input