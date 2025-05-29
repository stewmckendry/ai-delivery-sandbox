## 🧭 WP27 – Handoff to Next Pod (Phase 4+)

Welcome! You’re taking over from Iteration 3 of WP27, which focused on building and connecting toolchains for an end-to-end UX to generate policy artifacts with GPT.

This handoff includes everything you need to continue confidently.

## 🧠 What is PolicyGPT?

PolicyGPT is an AI-powered assistant designed to support teams in drafting high-quality gating artifacts for technology delivery. It integrates a custom GPT interface with a curated set of backend tools and memory systems that allow users to iteratively generate, revise, and assemble the components of approval-ready documents.

Unlike traditional documentation workflows, PolicyGPT offers a conversational, guided experience that adapts to user input, project context, and policy frameworks. It aims to accelerate artifact creation while maintaining the depth, structure, and traceability required by reviewers and approvers.

### 🚀 WP27 Mission
Create a frictionless and realistic user experience for generating policy artifacts using the existing tools and toolchains. Jam on the best UX by iteratively testing and evolving the system with real user flows and GPT integration.

This WP owns:
- Connecting the GPT interface to toolchains + tools
- Executing realistic user journeys end-to-end
- Documenting feedback, friction points, and enhancement needs
- Iterating rapidly to improve experience, accuracy, and modularity

---

### ✅ Status Recap

You are picking up from the end of Iteration 3, which established the foundational toolchains and logic for generating policy artifacts. The key components are:
- **Iteration 1 + 2**: Toolchain and tool validations, input ingestion, section generation
- **Iteration 3**: UX scaffolding and new logic for section generation, artifact chunking, and document-wide drafting
  - **New toolchains**: `generate_artifact_chain`, `global_context_chain`
  - **Key tools updated/added**: `generate_section_chain`, `fetchArtifactChunk`, `saveArtifactChunks`
  - **Chunking system**: Redis-based token-aware splitting with conditional reassembly

---

### 🧭 Your Mission (Test/Close Iteration 3, Deliver Iteration 4+)

You own Phase 4 onward:
- **Testing Iteration 3**: Validate end-to-end GPT experience using:
  - `generate_artifact_chain.py`
  - `generate_section_chain.py`
  - `global_context_chain.py`
  - Redis chunking tools, `saveArtifactChunks`, `fetchArtifactChunk`
  - finish off with `assemble_artifact_chain.py` to finalize and store artifacts in Drive
- **Iteration 4**: Implement stakeholder feedback stage of UX (see `policygpt_user_experience.md`):
  - Use / enhance `revise_section_chain` and `review_artifact_chain` 
  - Simulate feedback upload + GPT-driven revisions
  - Add checkpoints and persistence for review state
- **Iteration 5**: Implement kick off stage of UX (see `policygpt_user_experience.md`):
  - Use / enhance `inputPromptGenerator` 
  - User says what gate they need to prepare artifact for, and GPT calls tool to gather what needs to be prepared to guide the user through the process

---

### 📁 Key Files to Review

- UX design: `project/build/wps/WP27/policygpt_user_experience.md`
- Iteration 3 checklist (we're now on testing phase): `project/build/wps/WP27/iteration_3_task_list.md`
- Iteration 3 code to be tested (both with local script + wire to GPT):
  - app/engines/toolchains/IngestInputChain.py # unchanged, used to ingest inputs into the system, a prerequisite before the generation toolchains
  - app/engines/toolchains/global_context_chain.py # new toolchain for global context search that will inform 
  - app/engines/toolchains/generate_artifact_chain.py  # "auto-pilot" mode for generating full artifacts for review
  - app/engines/toolchains/generate_section_chain.py # "manual" mode for generating sections one at a time for review
  - app/engines/toolchains/assemble_artifact_chain.py # hasn't changed but is next part of the process to finalize the artifact after generate_artifact_chain.py or generate_section_chain.py
  - app/tools/tool_wrappers/saveArtifactChunks.py # new tool to save artifact chunks into Redis if document is too long in generate_artifact_chain.py 
  - app/tools/tool_wrappers/fetchArtifactChunk.py # new tool to fetch artifact chunks from Redis if document is too long in generate_artifact_chain.py
- Iteration 2 test plan + scripts + results to use as an example for Iteration 3+ testing:
  - project/build/wps/WP27/test_ingest_and_generate_section.py
  - project/build/wps/WP27/test_results_iteration_2.md

---

### 🛠 Instructions to Get Started

1. Review the reference files above to get up to speed by calling API tool fetch files in batch mode
2. Playback your understanding and any questions you have for your mission / work
3. Generate a plan for testing Iteration 3 end-to-end, starting locally, then with GPT. Commit to project/build/wps/WP27/. Include:
   - Test cases for each toolchain and tool (we want to test each of the Iteration 3 tools/toolchains individually, and then assembled together in a flow)
   - Expected inputs/outputs
   - Any additional logging or debugging needed
   - Instructions for human (me) to look up results in Redis and Drive
4. Generate a test script to automate running the Iteration 3 test plan.  Commit to project/build/wps/WP27/. Include:
   - Use `pytest` or similar framework
   - Ensure it can run locally and in CI
   - Capture logs and results for review (so we can clearly see what test case is running, the inputs, the outputs and pass/fail status)

---

### 💡 Tips + Lessons Learned

- Logs are clean and help a lot—use them!
- Chunking is automatic if document is long—Redis uses `artifact_id + session_id` as key
- Section order matters—use `gate_reference_v2.yaml` to determine correct sequence
- Most tools accept `session_id`, `artifact_id`, `gate_id`, `project_id`

---

### 🔁 Branch Info
- **Repo**: `ai-delivery-sandbox`
- **Branch**: `sandbox-curious-falcon`
- **Path**: `project/build/wps/WP27/`
- **Task_id**: `WP27-3`

See you in the next checkpoint!