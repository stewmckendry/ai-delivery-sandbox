# Scenario 2: End-to-End Test Summary

## ✅ Scenario Overview

This scenario covered the full end-to-end process:

1. Starting triage
2. Logging incident details
3. Assessing concussion risk
4. Educating on return-to-play stages
5. Logging activity check-ins
6. Inferring stage guidance
7. Exporting a PDF + FHIR bundle summary

---

## 🧪 Key Tools Used

* `get_triage_flow`
* `log_incident_detail`
* `assess_concussion`
* `get_stage_overview`
* `get_checkin_flow`
* `log_activity_checkin`
* `get_stage_guidance`
* `export_summary`

---

## ⚠️ Issues Encountered + Fixes

### 1. **SymptomLog mismatch in DB**

* **Issue:** `log_incident_detail` failed because `SymptomLog` model in `db_models.py` did not include `symptom_input`.
* **Fix:** Added missing field and committed model update.

### 2. **Field mismatch in `ConcussionAssessment`**

* **Issue:** `concussion_likely` used in tool; DB schema used `likelihood`
* **Fix:** Renamed field in `db_models.py` to match schema.

### 3. **Activity check-in tool failed with `UnrecognizedKwargsError: symptoms`**

* **Issue:** FastAPI expected a nested object, but GPT sent top-level keys.
* **Fix:** Flattened tool inputs and mimicked `log_incident_detail` pattern using `answers` dictionary.

### 4. **Stage inference tool broke**

* **Issue:** Inference model expected inputs that should have been retrieved from DB.
* **Fix:** Simplified tool to use only `user_id`, and adjusted logic to infer from DB.

### 5. **Export tool 500 error - invalid columns**

* **Issue:** DB column mismatches: `inference_mode`, `matched_factors` did not exist in `stage_result_export` table.
* **Fix:** Updated schema to align with expectations of PDF and FHIR generators.

### 6. **Broken PDF generation**

* **Issue:** PDF generated string and uploaded as .pdf, causing decode error.
* **Fix:** Switched to `WeasyPrint`, updated Dockerfile to support HTML-to-PDF rendering.

### 7. **Jinja errors in PDF generation**

* **Issue:** Tried calling `.items()` or subscripting ORM objects directly.
* **Fix:** Used dot notation, passed full ORM models to template.

---

## ✅ Final Outcome

* All tools work correctly and return expected outputs.
* PDF opens and renders properly.
* Export includes valid FHIR bundle and downloadable URL.

---

## 📁 Related Branch: `sandbox-silver-tiger`
