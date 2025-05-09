## 📌 Symptom Metadata Usage – Design Addendum

### 🎯 Purpose
To ensure consistency, validation, and richer functionality, we reference `reference/symptoms_*.yaml` when processing check-ins in Feature 2.

---

### 🔗 Symptom Source Files
- `reference/symptoms_physical.yaml`
- `reference/symptoms_emotional.yaml`
- `reference/symptoms_sleep.yaml`
- `reference/symptoms_red_flag.yaml`

Each file includes structured metadata for symptoms:
```yaml
- id: drowsiness
  name: "Drowsiness"
  severity: "low"
  risk_level: "medium"
  flags: [...]
  guidance: "..."
```

---

### ✅ How It’s Used
- **Validation**: `symptom_logger` will verify that all `symptom_id`s in the check-in exist in one of the YAMLs
- **Enrichment** (optional): metadata may be joined to support:
  - Flag recognition (e.g. red flags, triggers)
  - GPT response generation (via `guidance` or `risk_level`)
  - Scoring logic (mapping `severity` to weight)

---

### 📎 Future Enhancements
- A metadata cache can be loaded once and passed across tools
- Builder can evolve symptom maps without code changes

---

### 🔧 Builder Guidance
- Centralize a YAML loader for `symptom_logger`
- Consider refactoring into a service layer if reused
- Symptom `id`s must match exactly between user input and YAMLs

---