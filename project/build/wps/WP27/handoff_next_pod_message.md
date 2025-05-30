## 🚦 Handoff: WP27 Iteration 4 to Next ProductPod

### 🎯 Context
Welcome to WP27! You’re taking the baton from the previous ProductPod who completed Iteration 4 of the PolicyGPT experience.

PolicyGPT is a conversational interface that guides users through the generation, revision, and approval of policy artifacts. It connects backend tools and memory systems (SQL, Redis, Google Drive) to create a seamless, structured, and auditable document workflow.
d 
---

### ✅ Completed So Far
**Iterations 1–4 are complete:**
- 🔧 Iteration 1–2: Core tools and ingestion chains
- 🧩 Iteration 3: UX logic, Redis chunking, E2E flow
- 🛠️ Iteration 4: Stakeholder feedback tools, kickoff guides, and loadCorpus+research

Everything is integrated and ready for testing. All functionality for MVP is in place.

---

### 🧭 Your Mission
You are picking up from Iteration 4. Your tasks:
- ✅ **Test** the new/revised tools and toolchains from Iteration 4
  - Tools: `section_review_feedback`, `revise_section_chain`, `record_research`, `section_review_fetcher`, `inputPromptGenerator`
  - Chains: `assemble_artifact_chain`, `generate_section_chain`, `global_context_chain`
- ✅ **Test** the complete UX flow locally (CLI/pytest) and with the custom GPT (ChatGPT).
- ✅ **Create a Custom GPT for PolicyGPT**:
  - Name, description, instructions
  - Tooling (API actions)
  - Guide users through the UX flow documented in `policygpt_user_flow.md`
- ✅ **User Acceptance Testing**: Run UAT sessions, log feedback, recommend and implement enhancements iteratively. (this is the custom GPT testing)

---

### 🔍 Key Reference Files
> Call API tool `fetch_files` in batch mode to retrieve these files for review.
> These files contain the latest updates, tools, and UX flow documentation for PolicyGPT.
> Call in multiple batches if needed.

📁 PolicyGPT User Journey + Design Docs
project/build/wps/WP27/policygpt_user_flow.md
project/build/wps/WP27/wp27_part2_closeout.md

🔧 Tools and Toolchains (supporting UX flow)
app/engines/toolchains/assemble_artifact_chain.py
app/engines/toolchains/generate_artifact_chain.py
app/engines/toolchains/generate_section_chain.py
app/engines/toolchains/revise_section_chain.py
app/engines/toolchains/global_context_chain.py
app/engines/toolchains/IngestInputChain.py
app/tools/tool_wrappers/inputPromptGenerator.py
app/tools/tool_wrappers/loadCorpus.py
app/tools/tool_wrappers/queryCorpus.py
app/tools/tool_wrappers/record_research.py
app/tools/tool_wrappers/web_search.py
app/tools/tool_wrappers/goc_alignment_search.py
app/tools/tool_wrappers/saveArtifactChunks.py
app/tools/tool_wrappers/fetchArtifactChunk.py

📑 Prompt Templates (Examples)
prompts/generate_section_prompts.yaml
prompts/search_prompts.yaml

🧪 Test Plans / Scripts / Results (use same framework)
project/build/wps/WP27/test_ingest_and_generate_section.py
project/build/wps/WP27/test_results_iteration_3.md

🗃️ Other Key Docs
project/discovery/project_goals.md
project/reference/tool_catalog.yaml
project/reference/gpt_tools_manifest.json
project/reference/gate_reference_v2.yaml
project/system_design/db_schema_notes_v3.md

---

### 🛠 Instructions to Get Started

1. Review the reference files above to get up to speed by calling API tool fetch files in batch mode
2. Playback your understanding and any questions you have for your mission / work
3. Generate a plan for testing Iteration 4 tools/toolchains and the end-to-end user experience in `policygpt_user_flow.md`.  Start locally using  then with GPT. Commit to project/build/wps/WP27/. Include:
   - Test cases for each toolchain and tool (we want to test each of the Iteration 4 tools/toolchains individually, and then assembled together in a flow)
   - Expected inputs/outputs
   - Any additional logging or debugging needed
   - Instructions for human (me) to look up results in Redis and Drive and SQL DB
4. Generate a test script and test data to automate running the Iteration 4 test plan.  Commit to project/build/wps/WP27/. Include:
   - Use `pytest` or similar framework --> use same test framework as previous iterations
   - Ensure it can run locally and in CI
   - Capture logs and results for review (so we can clearly see what test case is running, the inputs, the outputs and pass/fail status)
   - Document in-line comments at top of script to explain the flow and purpose of each test case, and how to run the tests with pytest showing logs / inputs / outputs
5. Create a Custom GPT config guide for PolicyGPT:
   - Name, description, instructions
   - Tooling (API actions)
   - Guide users through the UX flow documented in `policygpt_user_flow.md`

---

## Helping GPT Discover Available Tools

- All tools are registered at runtime and exposed via a generic API path: `/tools/{tool_id}`
- GPT does not get a full catalog automatically — instead, you should preload it with:
  - A system message containing the tool catalog entries (name, description, schema)
  - Instructions for when and why to call each tool

### Tips:
- Use the `project/reference/tool_catalog.yaml` for readable descriptions and input schemas
- Refer to `project/reference/gpt_tools_manifest.json` for explicit field names and types (used in API calls)
- Pre-populate GPT instructions with sample tool calls so it understands the shape of requests
- If chaining tools (e.g., `generate_section_chain` → `saveArtifactChunks`), show example workflows

---

### 📂 Repo Info
- **Repo**: `ai-delivery-sandbox`
- **Branch**: `sandbox-curious-falcon`
- **Path**: `project/build/wps/WP27/`
- **Task_id**: `WP27-3`

---

### 💡 Tips from Last Pod
- Always pass `session_id`, `artifact_id`, `project_id` for traceability
- Redis stores interim results—check your keys if something seems off
- Section order follows `gate_reference_v2.yaml`
- 'pytest' scripts should use the same test framework as previous iterations
- Logs are clean and help a lot—use them!
- Check SQL DB tables for saved records, Redis for draft sections, and Google Drive for final artifacts as part of test results



Let’s make PolicyGPT amazing together. You got this 🚀