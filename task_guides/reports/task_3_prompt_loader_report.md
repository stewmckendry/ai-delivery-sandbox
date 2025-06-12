# Task 3 Review: YAML Prompt Loader

## ✅ Summary
Agent implemented a prompt loader that:
- Loads YAML files from the `app/prompts/` directory
- Extracts the `template` field
- Substitutes `{{ variable }}` placeholders using a basic regex-based renderer

## 📂 Files Created
- `app/prompts/loader.py`
- `app/prompts/summarize_lab_results.yaml`

## ▶️ Test Validation
```bash
python -m py_compile app/prompts/loader.py  # ✅ No syntax errors
```

To test in Python:
```python
from app.prompts.loader import load_prompt

lab_data = "\n- Glucose: 5.5 mmol/L\n- Cholesterol: 4.9 mmol/L"
print(load_prompt("summarize_lab_results", {"lab_data": lab_data}))
```

Expected output:
```
Summarize the following lab results:
- Glucose: 5.5 mmol/L
- Cholesterol: 4.9 mmol/L
```

## 💬 Feedback
- ✅ Clean implementation with clear function separation
- ✅ Handles missing variable edge case well
- 🟡 Consider using `jinja2` for more complex templating later

## 🔁 Next Step
Approved for use in prompt orchestration logic.
