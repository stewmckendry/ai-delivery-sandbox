## 🧪 Feature 4 – Design: Clinician Export (PDF + FHIR)

### 🎯 Goal
Provide a tool that generates exportable clinical summaries (PDF and FHIR) based on a user’s tracked recovery state.

---

### 📍 User Flow Mapping
1. User completes symptom logging (or stage inference)
2. GPT prompts: "Would you like a clinical summary to share with your coach or doctor?"
3. User confirms → triggers `export_summary` tool
4. Tool fetches tracker state + logs from DB
5. Tool returns:
   - PDF summary (HTML→PDF render)
   - FHIR Bundle JSON (Condition, Observation, CarePlan)

---

### 🧱 Data Mapping
**Source Models**: See [`db_schema_notes.md`](../feature_2_symptom_logging_stage_inference/db_schema_notes.md)  
**File Path**: `project/delivery/features/feature_2_symptom_logging_stage_inference/db_schema_notes.md`

| Source | Maps To | Format |
|--------|---------|--------|
| `tracker.state.stage` | `CarePlan.title`, `Condition.code` | string |
| `tracker.state.user_id` | `Patient.reference` | string |
| `symptom_log[].symptom_id` | `Observation.code.text` | string |
| `symptom_log[].severity` | `Observation.valueInteger` | int |
| `symptom_log[].timestamp` | `Observation.effectiveDateTime` | datetime |

---

### 🛠 Tool Design: `export_summary`
```python
@tool()
def export_summary(user_id: str) -> ExportResponse:
    """
    Fetches user's tracker data and returns a PDF + FHIR bundle for clinical use.
    """
    ...
```
- Inputs: `user_id`
- Outputs: `ExportResponse(pdf_url: str, fhir_bundle: dict)`
- File: `app/tools/export_summary.py`

---

### 🧰 Submodules
| File Path | Description |
|-----------|-------------|
| `app/tools/export_summary.py` | Main tool definition |
| `app/engines/epic_writer.py` | Converts DB → FHIR Bundle |
| `app/engines/pdf_renderer.py` | Converts HTML → PDF |
| `app/engines/schema_validator.py` | FHIR contract validation |
| `app/db/db_reader.py` | Fetch tracker + symptom data |

---

### 🧪 Test Strategy
- File: `test/test_export_summary.py`
- Tests:
  - FHIR JSON output contract test
  - PDF output render and structure
  - Sample input: tracked user with 3 symptoms + stage
  - Expected output: 1 Condition, N Observations, 1 CarePlan

---

### 🔄 Design Decisions
- Start with minimal viable FHIR (no full HL7 validation)
- PDF layout kept single-page for early MVP
- Endpoint returns both formats together for user clarity
- Pydantic `ExportResponse` used for OpenAPI validation

Let me know if you’d like a visual data flow diagram or export preview mock!