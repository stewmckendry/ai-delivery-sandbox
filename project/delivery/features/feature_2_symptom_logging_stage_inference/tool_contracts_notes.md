## 📑 Tool Contracts & Custom GPTs – Addendum

### 🎯 Purpose
To ensure that Custom GPTs use FastAPI tools correctly, we must clearly define and communicate the input format expectations for each tool.

---

### 📦 What’s at Risk
- GPT might omit required fields, use incorrect data types, or miss nested structures
- This leads to Pydantic validation failures or infinite retry loops

---

### 🛠️ Proposed Strategy
1. **Strict OpenAPI schema adherence**
   - Ensure all input models are declared with Pydantic
   - Include example payloads in docstrings or schema extensions

2. **Custom GPT instructions**
   - Inline tool tips: instruct GPT to use the exact schema with valid keys
   - Specify:
     - Required fields (e.g. `user_id`, `injury_date`)
     - Nested JSON objects (e.g. `tracker_state.answers`)
     - Allowed symptom IDs (validated against YAML)

3. **Validation-first design**
   - Reject early with clear errors
   - Log and surface validation failures for retraining

---

### 🧱 Builder Notes
- Consider writing a schema doc extractor for GPT-facing summary
- Embed OpenAPI-generated schemas into GPT tool config if needed
- Document constraints (like 0–5 scoring) inline and in tool metadata

---

### 📎 Related Files
- `symptom_logger.py`
- `get_stage_guidance.py`
- `models/symptoms.py`, `tracker.py`, `stage.py`
- `reference/symptoms_*.yaml`

---