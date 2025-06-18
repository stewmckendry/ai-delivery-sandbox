# 🧠 Task 307: Integrate Clinical Health Record Standards

## 🎯 Goal
Review the existing ETL and structured data model and propose how it can adopt health record standards such as FHIR resources or common medical terminologies (e.g., LOINC, SNOMED) to enhance:
- Interoperability with clinical systems
- Precision and structure in extracted records
- Reusability for sharing, charting, or integration into provider tools

---

## 🔍 Current State
- The pipeline currently populates a single table: `structured_records`
  - Fields: `text`, `type`, `source_url`, `portal`, `capture_method`
  - Text is extracted from HTML or PDF and lightly cleaned, not formally typed
- No standard clinical schema or coding is applied

---

## 🧪 Task Scope
1. Review `orchestrator.py`, `extractor.py`, and data models
2. Identify where to map:
   - Lab values → FHIR `Observation` or LOINC-coded entries
   - Visit summaries → FHIR `Encounter` or `Condition`
   - Clinical terms → SNOMED where feasible
3. Propose model/schema updates for structured storage (e.g., new tables or JSON blob formats)
4. Suggest optional export formats (e.g., FHIR bundles)

---

## 📈 Benefits
- Enables downstream sharing with providers and EHRs
- Makes records more structured and queryable
- Future-proofs the data model for research and clinical tools

---

## ✅ Done When
- Clear mapping plan proposed for each structured record type
- Suggested schema/model updates are documented
- FHIR-aligned or coded data export format proposed (even if not yet implemented)