# 🧬 Task 309: Extend ETL and DB Model for Additional Clinical Types

## 🎯 Goal
Expand the structured record model and ETL logic to detect and classify more clinical health data types beyond lab results and visit notes.

---

## 🧪 Scope of Work
### Update: `run_etl_from_blob` and `structured_records`
- Add classification support for these FHIR-mappable types:
  - `MedicationStatement` (e.g., Metformin)
  - `Condition` (e.g., Diabetes, Asthma)
  - `Procedure` (e.g., Surgery, Imaging)
  - `AllergyIntolerance`
  - `Immunization`
  - `VitalSigns` (e.g., BP, height, weight)
  - `DiagnosticReport` (wrap full document types)

### Tasks:
1. Update the `structured_records` model to include:
   - `clinical_type` (FHIR-style)
   - `code`, `code_system`, and `display` (for standard mappings)

2. In ETL pipeline (especially `extractor.py` and `run_etl_from_blob`):
   - Detect these types from plain text
   - Classify and tag with clinical type and potential coding
   - Use LOINC/SNOMED/RxNorm where mappings are possible

3. Ensure the `/ask` and `/summary` endpoints still function correctly with expanded record types

---

## ✅ Done When
- Blob uploads result in records categorized into 5+ clinical types
- Model supports code mapping fields for standards interoperability
- ETL summary includes breakdown by `clinical_type`
- Backward compatibility with lab and visit data is preserved