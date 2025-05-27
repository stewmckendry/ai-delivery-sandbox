## WP24 Toolchain Test Plan

### Objective
Ensure that the `generate_section_chain` and its individual tools function correctly and yield expected outputs. Confirm no regressions in `generate_artifact_chain`.

---

### Setup Steps
1. Checkout `sandbox-curious-falcon` branch.
2. Load sample data for:
   - `artifact`, `section`, `project_id`, `project_profile`
3. Ensure all environment variables for LLM APIs are set.
4. Ensure test user and session ID are initialized.

---

### Test Run Steps
#### A. Unit Tests for Individual Tools

**1. query_prompt_generator**
- Input: Valid `project_profile` and `memory`
- Expected Output: `{ "query": "..." }` (non-empty string)

**2. section_synthesizer**
- Input: Required context inputs, optional `context_summary`
- Expected Output: `raw_draft`, `draft_chunks`, `prompt_used`

**3. section_refiner**
- Input: `raw_draft`
- Expected Output: `raw_draft`, `prompt_used`

#### B. End-to-End Chain Test

**Toolchain: generate_section_chain**
- Input: All toolchain inputs including optional `context_summary`
- Expected Output: Valid reasoning trace, section saved via `save_artifact_and_trace`

#### C. Regression Test

**Toolchain: generate_artifact_chain**
- Input: Legacy inputs that previously worked
- Expected Output: Artifact generated without errors or skipped sections

---

### Inputs
Example test data will be hardcoded or mocked within test script.

---

### Expected Outputs
- All tests should complete without raising exceptions.
- Logs should confirm each step succeeded.
- Final artifact section should persist to DB with LLM-generated content.