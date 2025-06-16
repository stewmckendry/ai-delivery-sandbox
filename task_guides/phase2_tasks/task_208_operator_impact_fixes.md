# Task 208: Operator Testing Impact Fixes

## 🎯 Goal
Incorporate outcomes from hands-on testing with OpenAI Operator across real portals to enhance UX, ETL compatibility, and export reliability.

---

## 🛠 Subtasks

### 🔹 Task 208.1: Enhance HTML Extraction
- Ensure `extract_relevant_content()` and ETL can handle saved HTML snapshots with nested tables, embedded styles, or missing metadata
- Test with full-page Strava/TeamSnap HTML

### 🔹 Task 208.2: Allow PDF Input via Upload
- Update blob ingestion to support `.pdf` from print-to-PDF captures
- OCR where needed (add placeholder or note for Azure Form Recognizer pipeline)

### 🔹 Task 208.3: File Metadata Capture
- Store `source=operator`, `capture_method=html|pdf|screenshot`, and `user_notes` in structured record metadata for audit
- Update `insert_structured_records()` accordingly

### 🔹 Task 208.4: Copilot Instructions
- Add Operator troubleshooting tips to Copilot `/upload` and `/status` tool outputs
- Cover reCAPTCHA, Cloudflare, download methods

### 🔹 Task 208.5: Fallback for CSV Export
- If user requests CSV from Operator:
  - Suggest HTML save, local conversion, or manual copy
  - Add Copilot response to guide them

---

## 📂 Target Files
- `app/orchestrator.py`
- `app/extractor.py`, `app/cleaner.py`, `app/storage/models.py`
- `project/prompts/operator_templates.md`
- `project/docs/operator_guidance.md`

## 🔁 Notes
- See `project/docs/operator_testing_summary.md` for full context
- Label subtasks in PRs as `task_208.X`

## ✅ Outcome
Improves downstream reliability of Operator-derived files and preserves user control and consent.
