# Retrospective Tracker

## WP17b – Section Draft Generation

### ✅ What Went Well
- Solid architecture for toolchain and planner flow
- GPT integration was seamless and high quality
- End-to-end testability from PromptLog to DB
- Full documentation of steps, reusable reference WP

### 🤔 What Could Be Improved
- Auth context (`session_id`, `user_id`) should be injected earlier
- DB schema required fix (ArtifactSection PK change)
- Skipped embeddings due to `queryCorpus` tool unavailability
- Multiple places to register tools (registry, manifest, planner)

### 💡 Lessons & Recommendations
- Build CLI-first, test early, test often
- Keep GPT wrappers modular, composable
- Log everything with trace IDs and outputs
- Document planner-toolchain maps clearly
- Design DB for extensibility – avoid singleton PKs

## WP18 – Artifact Assembly and Routing

### ✅ What Went Well
- Strong modular architecture using toolchains and registries.
- Effective schema validation and logging throughout.
- Collaboration was smooth; feedback loop quickly applied to resolve issues.
- Test coverage was practical and caught meaningful edge cases.
- Final output quality is production-ready (clean format, ToC, markdown).

### 🤯 Challenges
- Escaping bugs in Jinja templates took time to trace.
- Early static templates interfered with dynamic rendering.
- Coordination of DB schema vs. doc fields required adjustments.
- Input validation improvements mid-way required refactoring.

### 💡 Lessons & Recommendations
- Dynamic over static templates reduces maintenance.
- Validate early using `parse_obj_as()` for consistent input models.
- Breakpoint logging helps diagnose pipeline bugs quickly.
- Use ordered trace to trace step-by-step logic and failures.

### 🔁 Improvement Areas
- Adopt snapshot-based unit testing for each tool.
- Auto-validate tool registry and manifest vs. implemented wrappers.
- Expand artifact schema documentation for easier onboarding.

## WP14 – External Source Integration

### ✅ What Went Well
- Successfully wrapped external web search using LLM-guarded retrieval
- Integrated cleanly with planner, manifest, and OpenAPI layer
- Tool supports param validation and default fallback behaviors

### 🤯 Challenges
- Risk of hallucinated or low-quality results in open web fetches
- Balancing token usage vs. info depth in search responses

### 💡 Lessons & Recommendations
- Limit query scope to reduce token overhead and API costs
- Always include fallback plan when no results are returned
- Use whitelist or scoring system to vet trusted sources

## WP7 – Project Profile Integration

### ✅ What Went Well
- End-to-end flow tested across ingestion, drafting, and final assembly
- Planner integration worked smoothly across chains
- Graceful fallbacks and null-safe schema
- Unit test script reflected real user behavior

### 🤯 Challenges
- Schema enforcement required multiple patch rounds
- Serialization issues with nested/logged fields (`Decimal`, `datetime`)
- Confusion between tool vs. toolchain caused rerouting

### 💡 Lessons & Recommendations
- Always orchestrate through `PlannerOrchestrator`
- Cast and clean profile fields before logging
- Build mocks and regression tests for all chains
- Introduce `project_profile` versioning + audit trail

## WP22 – GoC Alignment Search Tool

### ✅ What Went Well
- Strong cross-tool integration and clean modular structure
- Asynchronous corpus embedding prevented timeouts
- Tools reusable in both planner chains and standalone prompts
- Test automation validated all modes of use

### 🤯 Challenges
- First version of tools didn't follow class structure — refactoring needed
- Default queries lacked context — needed synthesized input
- Corpus loading UX requires improvement for cloud deployment

### 💡 Lessons & Recommendations
- Structure inputs with labels to manage prompt size
- Async loaders need status/polling support in prod
- Consider confidence scoring + filtering for corpus results
- Enable multilingual queries and corpus segmentation

## WP1a – Scaffolding + Assembly

### ✅ What Went Well
- Strong system design alignment and modular tool structure
- Early CLI validation enabled fast iteration
- Generalizable pipeline structure

### 🤯 Challenges
- Schema mismatches and unclear section metadata handling
- Output writing logic missing initially

### 💡 Lessons & Recommendations
- Include real YAML tests early
- Use CLI `--ref_path` override
- Output both `.md` and `.json` samples

---

## WP3a – Planner + Memory Layer

### ✅ What Went Well
- CLI-first build made test-driven progress smooth
- Replay and logging features were valuable
- Trace YAML and schemas reused in multiple WPs

### 🤯 Challenges
- Toolchain wiring and DB setup came late
- YAML planner task trace should be standard

### 💡 Lessons & Recommendations
- Add end-to-end CLI test runner
- Use hash-based filenames for trace logs

---

## WP3b – Tool Wrapping + API

### ✅ What Went Well
- Modular and schema-driven registry built with full CLI/API/GPT support
- Git-based loading was robust and error handling worked
- Clear documentation helped future pods

### 🤯 Challenges
- Schema and tool stubs needed earlier alignment
- Tool registry merge and validation workflows caused drift

### 💡 Lessons & Recommendations
- Use WP3b’s tool registry as system of record
- Add metadata fields (`doc_id`, `section_id`) early
- Output Markdown and JSON consistently

---

## WP9 – Input Ingestion

### ✅ What Went Well
- Unified ingestion flow across file, link, and text inputs
- Reliable trace + snapshot logging for memory layer
- Tool structure supported consistent input handling

### 🤯 Challenges
- Runner vs. tool duplication created bugs
- DB schema drift delayed integration
- PyODBC error logs unclear

### 💡 Lessons & Recommendations
- Use runners for `structure_input` logic
- Align schema across code, YAML, and DB
- Test ingestion tools via CLI early

---

## WP16 – Input Prompt UX Layer

### ✅ What Went Well
- Input UX built to spec with clean vector DB integration
- All prompt tools validated and tested
- GPT- and planner-ready schemas confirmed

### 🤯 Challenges
- Vector DB setup issues delayed cloud testing
- Prompt record logging lacked session view UI
- Schema validation errors not surfaced clearly

### 💡 Lessons & Recommendations
- Build prompt-to-draft trace viewer
- Integrate highlighter with corpus search
- Suggest prompts via intent tagging

---

## WP23 – Section Revision from Feedback

### ✅ What Went Well
- Modular architecture scaled well across tools
- Summarizing section inputs improved LLM comprehension
- CLI-first implementation enabled test-driven development
- GPT wrappers supported composability and reuse

### 🤔 What Could Be Improved
- LLM responses not always compliant with feedback nuance
- Manual edits required post-check to match tone/style
- Feedback classification could misroute ambiguous input
- Many tools involved → high coordination overhead

### 💡 Lessons & Recommendations
- Keep prompt design abstracted for updates
- Consider prompt memory limits and minimize token bloat
- Add UX layer for multi-feedback aggregation and selection
- Implement a unified validation + QA harness

---

## WP24 – Generate Full Artifact

### ✅ What Went Well
- Strong modularization of tools and LLM usage.
- Standardized prompt templates improved reusability.
- Schema enforcement via tool registry prevented runtime errors.
- Testing framework ensured reliability and regression control.

### 🤔 What Could Be Improved
- Initial commits caused regressions due to unscoped changes—need stricter scope discipline.
- More frequent integration testing would have surfaced interface mismatches earlier.
- Better tracking of which tools have updated schemas to streamline tool_catalog maintenance.

### 💡 Lessons & Recommendations
- Enforce stricter change isolation in complex toolchains.
- Add test cases for each prompt YAML key during validation.
- Auto-generate tool_catalog/manifest entries from schemas.

## WP27 – E2E UX Testing & Enhancements

### ✅ What Went Well
- 🎯 Clear mission scope centered on realistic drafting flows
- 🔁 Smooth iteration and toolchain chaining
- 🧱 Effective chunking implementation using Redis
- 🧠 Reuse of `plan_sections` helped enforce draft order
- 🧪 All toolchain steps tested before orchestration

### 🤔 What Was Surprising
- Chunking required more design effort than expected
- Redis plugin integration in dev environment took extra setup
- Chunking proved essential due to token limits in end-to-end flow

### 🚧 What Could Improve
- Earlier storyboard of end-user flow to identify tool gaps
- Enhanced UX trace during GPT execution
- Clearer boundary between persistent and ephemeral memory

### 💡 Key Learnings
- Orchestration critical for context-aware drafting
- Chunk-level orchestration improves memory and performance
- Global context should be summarized once and reused

### 🛣️ What’s Next
- Build revision and feedback toolchain
- Add checkpoints, scoring, and review mode
- E2E flow test with simulated human feedback