# Task 25 Review: LLM Content Extraction and Tagging

## ✅ Summary
Implements an HTML parser that:
- Strips visible text from raw HTML
- Chunks large pages for token-safe LLM calls
- Prompts the LLM to extract only patient-relevant content and classify each item
- Tags results with type and source URL

## 📂 Files
- `app/extractor.py`
- `tests/test_extractor.py`

## 🧪 Test
```bash
pytest -q tests/test_extractor.py
```
- ✅ Confirms correct chunking and classification
- ✅ Validates response format (type, text, source_url)

## 🔁 Output
```json
[ { "type": "lab_result", "text": "Sodium 140 mmol/L", "source_url": "https://..." } ]
```

## 🔄 Prompt Template
```text
Extract only patient-relevant content from this page. Classify it as one of: lab_result, visit_note, imaging_report, billing_info. Return JSON...
```

## 💬 Feedback
- ✅ Modular and robust against noisy HTML
- ✅ Output is taggable and RAG-ready
- 🟡 Consider fallback on malformed LLM JSON or retries

## 🚀 Ready to classify and extract structured content for downstream use