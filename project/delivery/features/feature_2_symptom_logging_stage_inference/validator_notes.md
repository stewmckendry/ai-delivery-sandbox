## ✅ Symptom Validator Integration – Addendum

This addendum documents how to use the centralized YAML validator for symptom IDs.

---

### 🔧 Tool Location
- **File**: `app/tools/validator.py`
- **Functions**:
  - `load_known_symptom_ids()` → returns `Set[str]`
  - `validate_symptom_ids(input_ids: Set[str])` → raises error if invalid

---

### 🧠 Why It Matters
- Ensures only valid `symptom_id`s are used in check-ins
- Prevents malformed tracker states
- Standardizes schema enforcement across tools

---

### 🔁 Where To Use It
#### In `symptom_logger.py`
Replace inline check:
```python
for sid in payload.symptoms.keys():
    if sid not in KNOWN_SYMPTOMS:
        raise ValueError(f"Unknown symptom ID: {sid}")
```
With:
```python
from app.tools.validator import validate_symptom_ids
validate_symptom_ids(set(payload.symptoms.keys()))
```

---

### 📎 Notes
- You can call `load_known_symptom_ids()` once and cache if needed
- All YAMLs are pulled remotely from GitHub
- Extendable to validate tracker flow or stages

---