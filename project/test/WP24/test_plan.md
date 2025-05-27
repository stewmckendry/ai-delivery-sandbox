# WP24 Toolchain Test Plan

## Objective
Verify the correct functionality and integration of new tools and toolchains implemented in WP24. Ensure tool interfaces, prompt rendering, and section processing work individually and in combination. Also, confirm regression for assemble_artifact_chain.

## Setup Steps
1. Checkout the `sandbox-curious-falcon` branch.
2. Ensure environment variables for OpenAI API keys are set.
3. Ensure all necessary packages are installed (`dotenv`, `jinja2`, `pydantic`, etc).

## Test Run Steps
Run the script:
```bash
python project/test/WP24/test_script.py
```

## Test Coverage
### Unit Tests
1. **query_prompt_generator**
   - Input: project_profile and memory list.
   - Expect: Valid search query string.

2. **section_synthesizer**
   - Input: section metadata, profile, memory, corpus, alignment, web summary.
   - Expect: raw draft with source breakdown.

3. **section_refiner**
   - Input: raw_draft text.
   - Expect: polished/refined draft.

4. **refine_document_chain**
   - Input: long formatted markdown string.
   - Expect: improved clarity, with chunking if needed.

### Integration Tests
5. **generate_section_chain**
   - Input: artifact ID, section ID, project profile, context_summary.
   - Expect: full trace, persisted section, final refined draft.

6. **assemble_artifact_chain**
   - Input: artifact ID, gate ID, project profile.
   - Expect: full markdown, trace, saved outputs to ArtifactSection and Drive.

## Expected Output
- Each tool should return structured dict outputs.
- Trace objects should contain tool output logs.
- Logs in stdout for debug.

## Regression
- Ensure assemble_artifact_chain behavior and outputs are consistent with pre-refactor version.
- DocumentBody before and after refine step should show improved structure, not hallucinations.