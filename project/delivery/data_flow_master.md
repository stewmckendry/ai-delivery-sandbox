...

---

## 🧩 SYMPTOM LOGGING ADDENDUM

### Why This Matters
- Symptom check-ins are a central part of tracking concussion recovery.
- Structured YAML defines symptoms used in triage and assessment tools.
- Current logging is inconsistent, under-specified, and missing metadata fields.

### Current Issues
- `SymptomLog` uses reserved field `metadata`.
- Fields like `reporter_role`, `incident_context`, etc., only captured during triage.
- No structured schema like `triage_map.yaml` exists for symptom check-ins.
- Validation against `symptoms_*.yaml` is ad hoc, lacks audit trail.

### Fix Plan
1. **Model Updates**
   - Rename `metadata` → `log_metadata` in `SymptomLog`
   - Add missing fields: `incident_context`, `reporter_role`, etc.

2. **Schema and Validation**
   - Introduce `symptom_log_map.yaml` as structured follow-up schema
   - Add validation script comparing model vs YAML field alignment

3. **Codebase Refactor**
   - Move all YAML parsing to `symptom_library.py`
   - Use `SymptomDefinition` type to unify structure across tools

4. **Downstream Use**
   - Use shared definitions in `export_to_sql`, `pdf_renderer`, `epic_writer`
   - Power BI exports should pull both `symptoms` and `log_metadata`

5. **Join Strategy**
   - `SymptomLog` joins to `IncidentReport` via `user_id` + timestamp proximity
   - Minimal intentional overlap — scope is different (incident vs check-in)