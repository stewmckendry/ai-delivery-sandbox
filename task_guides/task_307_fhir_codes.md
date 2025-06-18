# Codex Agent Task: Add FHIR Code Support

## 🎯 Goal
Store standard code data and FHIR resources alongside existing health records.

## 📂 Target Files
- `app/storage/models.py`
- `app/storage/structured.py`
- `tests/test_models.py`

## 📋 Instructions
1. Extend `LabResult` with a nullable `loinc_code` column.
2. Extend `VisitSummary` with a nullable `snomed_code` column.
3. Add a new `FHIRResource` model with:
   - `id`, `resource_type`, `resource_json`, `record_type`, `record_id`.
4. Provide helper `insert_fhir_resources(session, resources)` in
   `app/storage/structured.py`.
5. Update unit tests to ensure tables create successfully and rows insert.

All work should be committed on branch `sandbox-curious-fox`.
