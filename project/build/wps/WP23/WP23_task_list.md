# WP23 Task List: Artifact Refinement from Feedback

## ✅ Setup and Planning
- [x] Fetch WP definition and reference files
- [x] Draft and commit `WP23_toolchain_plan.md`
- [x] Update design plan with feedback handling, routing logic, Drive sync logic

## 🚧 Build Tasks
- [x] Create `revise_section_chain.py` orchestrator
- [x] Build `feedback_mapper.py` for section targeting + change classification
- [x] Build `section_rewriter.py` using prompt variants from `revision_prompts.yaml`
- [x] Implement `manualEditSync.py` for pasted revisions
- [x] Build `feedback_preprocessor.py` to normalize and classify feedback
- [x] Add `revision_checker.py` to flag hallucinations or excessive edits
- [x] Enhance `revise_section_chain.py` to support split_feedback and type per item
- [x] Add save logic for `verbatim` flow
- [x] Fix section override logic and skip feedback_mapper if provided
- [x] Add optional `additional_suggestions` return in `section_rewriter`

## 🧪 Testing
- [ ] Scaffold `test_revise_section_chain.py`
- [ ] Write tests: input mapping, prompt selection, revision quality, trace validation

## 🗃️ Integration and Logging
- [x] Hook up logging to `PromptLog`, `ArtifactSection`, and `ReasoningTrace`
- [x] Retrieve current section from `ArtifactSection`
- [x] Log `feedback_text` using new `DocumentFeedback` model
- [ ] Add to `planner_orchestrator.py`
- [ ] Add to `tool_catalog.yaml`
- [ ] Add to `manifest.json`

## 🧭 UX Integration
- [ ] Confirm triggers from GPT chat, uploads, and corpus updates
- [ ] Ensure graceful fallback for ambiguous input types

## 🧩 Feedback Infrastructure
- [x] Create `DocumentFeedback` model file
- [x] Add SQL schema for `document_feedback`
- [ ] Update `db_schema_v3.md`
- [x] Implement `save_feedback` handler in `memory_sync.py`

## 🔍 Enhancements
- [x] Add compliance validator via `revision_checker`
- [x] Add `feedback_preprocessor` output support for list with individual revision types
- [x] Return suggestions on other edits in `section_rewriter`

## 🔚 Finalization
- [ ] Request Pod Lead review
- [ ] Final polish + documentation

---

[View Toolchain Plan](https://github.com/stewmckendry/ai-delivery-sandbox/blob/sandbox-curious-falcon/project/build/wps/WP23/WP23_toolchain_plan.md)