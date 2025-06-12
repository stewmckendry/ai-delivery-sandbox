# Task 28: Full ETL Test Script + Integration Check

## 🎯 Goal
Implement a test runner script (`run_portal_test.py`) to exercise the entire ETL pipeline for a portal and validate that `run_etl_for_portal()` integrates the full system.

## 📂 Target Files
- `scripts/run_portal_test.py`
- Optionally update: `app/orchestrator.py`

## 📋 Instructions
- Build a CLI tool that:
  - Accepts `--portal`, `--depth`, `--debug`
  - Runs `run_etl_for_portal(portal)`
  - Tracks start/end time
  - Logs a summary to `logs/portal_runs/{portal}_{timestamp}.json`
- Validate that:
  - `crawler`, `extractor`, `cleaner`, `summarizer`, and storage are all invoked as expected
  - Environment vars like `MAX_DEPTH` work
  - Screenshots + logs are saved if challenges occur

## 🧪 Test
- Run with mock portal and confirm all stages complete
- Capture output logs and sample summaries

## ✅ What to Report Back
- Test runner CLI file
- Any changes to orchestrator for pipeline completeness
- Sample log output and runtime info

Refer to `task_27_pipeline_test_harness_and_flow.md` for context.