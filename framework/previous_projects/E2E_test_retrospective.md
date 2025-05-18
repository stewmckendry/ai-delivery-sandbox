# Retrospective: Scenario 2 End-to-End Test

## What Went Well

* ✅ **Full flow tested:** Triaged users from initial report to full recovery export.
* ✅ **Tool schemas clarified:** Validated and updated OpenAPI schemas.
* ✅ **PDF generation successful:** Introduced real PDF output using WeasyPrint.
* ✅ **Resilient design:** Reused working `answers` pattern from triage to simplify activity logging.
* ✅ **Issue debugging improved:** Added server-side logging and FastAPI error printing.

## What Was Hard

* ❌ **FastAPI schema mismatch:** Took multiple attempts to align Pydantic with GPT parameter style.
* ❌ **Silent failures:** Initial errors lacked detail, making root cause unclear.
* ❌ **DB drift:** Schema in `db_models.py` diverged from SQL tables (e.g. `inference_mode`, `matched_factors`).
* ❌ **PDF corruptions:** Encoding issue with text-based PDF caused unreadable files.
* ❌ **Limited test automation:** All tests done manually; no automated regressions or validators.

## Fixes Made

* Flattened schema inputs for GPT compatibility
* Switched from fake `.pdf` to actual PDF rendering with full dependency setup
* Refactored export tools to use latest DB schema and model updates
* Strengthened DB model alignment with SQL definitions
* Introduced route logging and error capture for better diagnostics

## Opportunities Next Time

* Add automatic schema validation against SQL
* Introduce E2E test harness (with example payloads and expected outputs)
* Consider mock DB or sandbox mode to run multiple tests in parallel
* Add retry/validation layers for fragile tool calls
* Avoid redundant inputs to tools (e.g., injury date passed when it already exists in DB)
