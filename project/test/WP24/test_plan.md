## WP24 Toolchain Test Plan

### Objective
Validate the functionality, integration, and regression behavior of all tools and toolchains implemented or updated in WP24. This includes individual tool outputs and full chain orchestration.

### Setup Steps
1. Ensure local environment is running with necessary dependencies.
2. Set `OPENAI_API_KEY` as environment variable.
3. Load test project and artifact data into the database.
4. Confirm tool_catalog is up to date with new entries.

### Test Runs

#### Test 1: `query_prompt_generator`
- **Input**: Project profile and memory
- **Expected Output**: A rich, concise query string

#### Test 2: `section_synthesizer`
- **Input**: Project profile, memory, corpus, alignment, web summary
- **Expected Output**: Structured draft content with dense paragraphs

#### Test 3: `section_refiner`
- **Input**: Raw draft text
- **Expected Output**: Refined and polished text

#### Test 4: `generate_section_chain`
- **Input**: Artifact ID, Section ID, Project profile
- **Expected Output**: Full section draft saved to `ArtifactSection`

#### Test 5: `assemble_artifact_chain`
- **Input**: Artifact ID
- **Expected Output**: Full artifact body assembled, refined, saved to `ArtifactSection`

#### Test 6: `generate_full_artifact_chain`
- **Input**: Project and artifact ID, Gate, and user metadata
- **Expected Output**: All sections synthesized, refined, and assembled into final output in `ArtifactSection`

#### Regression Test: `revise_section_chain`
- **Input**: Feedback on section content
- **Expected Output**: Revised content saved, changes logged and validated

### Notes
- Each test will be run via Python test script.
- Logs and output will be printed and reviewed for verification.
- Regression tests will compare previous vs. current behavior.

### Expected Artifacts
- Updated `ArtifactSection` entries
- Reasoning traces for each toolchain run
- Printed test results for each step
