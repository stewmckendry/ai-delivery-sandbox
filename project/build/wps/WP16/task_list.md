- [x] T1a – Design input prompt UX layer and metadata schema
- [x] T1b – Build inputPromptGenerator tool
- [x] T1c – Build inputChecker tool (Phase 1: Static Evaluation)
- [x] T1d – Patch upload input tools to pass structured metadata
- [x] T1e – Patch log_tool_usage to write metadata
- [ ] T2 – Build inputChecker tool (Phase 2: LLM Evaluation)
- [ ] T3 – Build `loadCorpus` tool for loading and embedding documents
- [ ] T4 – Generate UX messages, tool metadata, and starter messages for GPT
- [ ] T5 – Commit and push tool catalog updates, prompt schema reference, and integration notes
- [ ] T6 – Final test run and snapshot export of a sample session
- [ ] T7 – Design GPT Review UX Interface (Input Summary + Confirm to Draft)
- [ ] T8 – Completion note and lead pod update

💡 CR Scope Additions (Handled in T1c):
- Strategy to capture input mode using GPT conversation and memory
- Documentation for GPT config team to implement starter messages + system prompt
- Spillover coordination flagged to Pod Lead

💡 New Deliverable (Handled in T7):
- GPT review interface spec to preview user input before draft generation, per `dense_artifact_generation.md`

---

🔧 Patch Plan
- P1. Add optional metadata dict to structured_input_ingestor.py
- P2. Patch all upload tools to accept + pass metadata
- P3. Patch inputChecker to write metadata to PromptLog
- P4. Patch memory_sync.py log_tool_usage with metadata support
- P5. [PENDING] Populate PromptLog full_input_path / full_output_path with JSON metadata blob
- P6. [PENDING] Add tests for tool ingestion and trace logging validation
- P7. [DONE] Send CR cascade message to Pod Lead