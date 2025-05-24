# WP18 – Test Plan for `assemble_artifact` Toolchain

## 🎯 Objectives
- Validate the end-to-end functionality of the `assemble_artifact` toolchain
- Ensure supporting tools (`loadSectionMetadata`, `formatSection`, `mergeSections`, `finalizeDocument`, `commitArtifact`) function correctly in sequence
- Confirm logs and ReasoningTrace are recorded
- Ensure fallbacks and dynamic behaviors (like template generation) perform as expected

## 🧪 Setup Steps

1. **Populate Database with Dummy Sections**
   - Insert `ArtifactSection` records for a dummy artifact ID `investment_proposal_concept` and gate ID `0`.
   - Each section should have a `section_id`, `text`, and valid `status='draft'`.

2. **Set Environment**
   - Activate the virtual environment
   - Ensure the following packages are installed:
     ```bash
     pip install -r requirements.txt
     ```

3. **Load Sample Data**
   - Optionally use SQL script or ORM code to seed test data.
   - Ensure test DB connection and models are set up.

4. **Verify Gate Reference Accessibility**
   - Confirm access to live URL: https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/project/reference/gate_reference_v2.yaml

## 🧪 Test Steps

### 1. Assemble Artifact Toolchain Invocation
**Command:**
```bash
python -c "from app.engines.planner_orchestrator import PlannerOrchestrator; print(PlannerOrchestrator().run('assemble_artifact', {'artifact_id': 'investment_proposal_concept', 'gate_id': '0', 'version': 'v0.1'}))"
```
**Expected Result:**
- Output includes `final_output` and `trace`
- Local file is saved and its path is in output
- Markdown document includes headers for each section

### 2. Log Validation
- Check `prompt_log` and `reasoning_trace` tables for entries
- Validate ReasoningTrace includes all 5 steps with tool names

### 3. Dynamic Template Validation
- If no template exists in `artifact_templates/`, dynamic fallback should generate one
- Confirm template content includes section titles

### 4. Error Handling
**Test:** Supply an invalid `artifact_id`
**Command:**
```bash
python -c "from app.engines.planner_orchestrator import PlannerOrchestrator; print(PlannerOrchestrator().run('assemble_artifact', {'artifact_id': 'nonexistent_artifact', 'gate_id': '0'}))"
```
**Expected Result:**
- Fails gracefully with message indicating template or sections not found

## ✅ Completion Criteria
- End-to-end toolchain completes without error for a valid test case
- Logs and trace captured
- Output file matches expected structure
- Fallback logic tested for dynamic template
- Errors gracefully handled
