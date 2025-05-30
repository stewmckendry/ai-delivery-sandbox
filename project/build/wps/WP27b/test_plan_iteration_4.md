# ✅ WP27 Iteration 4 — PolicyGPT Test Plan

## 🎯 Purpose
Validate end-to-end functionality for the PolicyGPT MVP, covering all tools and toolchains introduced in Iteration 4, aligned to the user flow.

---

## 🧪 Test Strategy
Tests are modular and sequential. Each test case corresponds to a step in the UX flow and exercises a specific tool/toolchain. Common test data (e.g., `project_id`, `session_id`) is used across all test cases.

---

## 🔢 Test Variables
```python
project_id = "test_policy_project"
session_id = "test_session_042"
user_id = "user_admin"
artifact_id = "investment_proposal_concept"
gate_id = 3
section_id = "problem_context"
```

---

## 📋 Test Cases

### Test 1 – Prompt Generator
- **Tool**: `inputPromptGenerator`
- **Inputs**: `section_id`, `artifact_id`, `gate_id`
- **Expected**: Returns tailored input prompts for a given section

### Test 2 – Upload and Ingest
- **Chain**: `IngestInputChain`
- **Inputs**: Text content + metadata (above)
- **Expected**: Uploads text, indexes for memory

### Test 3 – Record Research
- **Tool**: `record_research`
- **Inputs**: Session metadata + source note
- **Expected**: Stores note, traceable in SQL/Redis

### Test 4 – Generate Section Draft
- **Chain**: `generate_section_chain`
- **Inputs**: Section id + stub profile + metadata
- **Expected**: Returns draft text with intent coverage

### Test 5 – Review Section
- **Tool**: `section_review_feedback`
- **Inputs**: Raw draft text + goals
- **Expected**: Generates structured feedback

### Test 6 – Revise Draft
- **Chain**: `revise_section_chain`
- **Inputs**: Draft + feedback + metadata
- **Expected**: Revised draft text

### Test 7 – Fetch Review State
- **Tool**: `section_review_fetcher`
- **Inputs**: Section id, session id
- **Expected**: Returns stored feedback + prior version

### Test 8 – Global Context Summary
- **Chain**: `global_context_chain`
- **Inputs**: Project_id, artifact_id, gate_id
- **Expected**: Returns global summary for use by drafting chains

### Test 9 – Assemble Final Artifact
- **Chain**: `assemble_artifact_chain`
- **Inputs**: session_id, artifact_id, gate_id
- **Expected**: Final document + Drive link

---

## 📊 Validation Guidance
- Check Redis for stored chunks: key = `session_id:artifact_id`
- Query SQL for inputs/research: see schema in `db_schema_notes_v3.md`
- Confirm Google Drive artifact via returned link

---

## 🧼 Debugging Aids
- Print logs at each step
- Capture `tool_input`, `tool_output`, and errors
- Include traceback and session metadata

---

## 📁 Output Files
- `test_iteration_4.py`: test runner script
- `test_log_iteration_4.txt`: logs for manual review