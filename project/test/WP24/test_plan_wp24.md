**WP24 Test Plan**

**Objective:**
Validate the functionality and integration of tools and toolchains implemented in WP24. Confirm that all individual tools operate as expected, toolchains run end-to-end, and previous core functionality (e.g., `generate_artifact_chain`) is not regressed.

---

**Test Setup:**
- Use `sandbox-curious-falcon` branch.
- Ensure required test data is mocked within the test script.
- Confirm LLM API key is configured for local run.

---

**Test Run Steps:**
1. Run `test_wp24_toolchain.py` from `project/test/WP24/`.
2. Observe terminal logs for test outputs.
3. Review any exceptions or errors and validate correctness of outputs.

---

**Test Coverage:**

**[Tool Tests]**
1. `query_prompt_generator`
   - Input: project profile + memory
   - Output: single search query string

2. `section_synthesizer`
   - Input: artifact, section, project profile, memory, web/corpus/alignment/context inputs
   - Output: drafted section

3. `section_refiner`
   - Input: raw_draft
   - Output: refined draft

**[Toolchain Tests]**
4. `generate_section_chain`
   - Input: project profile, artifact, section, session/user/project/gate
   - Output: ArtifactSection and ReasoningTrace saved

5. `generate_full_artifact_chain`
   - Input: project_id, session_id, user_id
   - Output: Artifact with full sections generated and stored

**[Regression Test]**
6. `generate_artifact_chain`
   - Input: existing project and artifact
   - Output: updated sections based on saved draft states (assumes existing coverage)

---

**Expected Output:**
- Valid outputs printed for each tool.
- Trace steps confirmed for toolchains.
- Final save results include ArtifactSection + ReasoningTrace
- No unhandled errors or schema mismatches.