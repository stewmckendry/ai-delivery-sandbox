# Spillover Tracker

Tracks unfinished or deferred work from each WP.

| Item | Source WP | Reason for Deferral | Suggested Owner | Status |
|------|-----------|----------------------|------------------|--------|
| T7: Validate and trace against gate formatting rules | WP1a | Out of WP1a scope (focus on pipeline structure) | WP2 or WP5 | Unassigned |
| Use memory for section expansion | WP1a | Stubbing only in WP1a | WP2 | Unassigned |
| Integrate tools (e.g., cost tables) in expansion | WP1a | Deferred for future tool integration | WP3 | Unassigned |
| Enable GPT-driven document synthesis | WP1a | Design placeholder only | WP2/WP4 | Unassigned |
| Final content QA + style validation | WP1a | Planned in later stages | WP5 | Unassigned |
| Wire DB + expose models via API | WP3a | Local file-based only | WP4 | Unassigned |
| Implement real tool logic | WP3b | Registry stubs only | Various per tool | Assigned (per tool tracker) |
| `compose_and_cite` chain (no WP owns fully) | WP3b | Complex, spans multiple pods | WP4, WP5, WP6 or new WP | Unassigned |
| Connect ingestion to GPT input UI | WP9 | Ingestion logic built, UI not wired | WP16 | Unassigned |
| Integrate ingestion logs with Planner | WP9 | Planner unaware of ingestion | WP2/WP3a | Unassigned |
| Use PromptLog and SessionSnapshot in doc gen | WP9 | Data present, not yet used downstream | WP2/WP4 | Unassigned |
| Cloud storage of logs (Drive or S3) | WP9 | Currently writes to disk only | WP6 or new infra WP | Unassigned |
| Update `trace_utils.write_trace` for cloud | WP9 | Local path only | WP3c or WP6 | Unassigned |
| Update `createSessionSnapshot` for cloud | WP9 | Local-only logging | WP3c or WP6 | Unassigned |
| Input mode support in session logging | WP16 | Requires metadata tagging | WP3a | Unassigned |
| Mode-aware logic in document assembly | WP16 | Requires mode detection | WP4/WP6 | Unassigned |
| System prompt + starter wiring for modes | WP16 | Needs GPT config setup | GPT_Config | Unassigned |
| UI toggle metaphor guidance | WP16 | Needs cross-pod UX clarity | WP12 | Unassigned |
| `/tools/compose_and_cite.py` | WP12 | Assigned but not yet implemented | WP4 | Unassigned |
| `/tools/revise_section.py` | WP12 | Assigned but not yet implemented | WP8 | Unassigned |
| `/tools/get_token_usage.py` | WP12 | Assigned but not yet implemented | WP2 | Unassigned |
| `/tools/validate_section.py` | WP12 | Assigned but not yet implemented | WP5 | Unassigned |
| `/tasks/confirm_draft_start` | WP12 | Assigned but not yet implemented | WP6 | Unassigned |
| `/ui/gpt_review_interface.md` | WP12 | Assigned but not yet implemented | WP16 | Unassigned |
| `/planner/templates/planner_task_trace.yaml` | WP12 | Assigned but not yet implemented | WP3c | Unassigned |
| `/db/schemas/prompt_log.sql` | WP12 | Assigned but not yet implemented | WP9 | Unassigned |
| `/db/schemas/artifact_section.sql` | WP12 | Assigned but not yet implemented | WP6 | Unassigned |
| `/db/schemas/reasoning_trace.sql` | WP12 | Assigned but not yet implemented | WP7 | Unassigned |
| `/db/schemas/document_version_log.sql` | WP12 | Assigned but not yet implemented | WP6 | Unassigned |
| `/yaml/validation_log.yaml` | WP12 | Assigned but not yet implemented | WP5 | Unassigned |
| `/yaml/project_profile.yaml` | WP12 | Assigned but not yet implemented | WP1b | Unassigned |
| `/yaml/gate_reference.yaml` | WP12 | Shared reference file | WP1a | Maintained |
| `/system/docs/dense_artifact_generation.md` | WP12 | Design doc, no further action | WP12 | Maintained |
| `queryCorpus` for semantic doc search | WP16 | Not in original scope | WP10 or new WP | Unassigned |
| Enhance `inputChecker` with LLM mode | WP16 | LLM-based mode proposed in CR | WP4 or follow-on WP | Unassigned |
| GPT config + UI wiring for starter prompts | WP16 | Config not finalized | GPT_Config | Unassigned |
| Add section metadata chunking to `loadCorpus` | WP16 | Feature incomplete | WP16 or WP9 | Unassigned |
| Implement `compose_and_cite` from PromptLog | WP16 | Draft generator not started | WP4 or WP6 | Unassigned |
| Implement `queryCorpus` for embedding search + memory recall | WP17b | Required for memory lookup; deferred due to tool not being built yet | WP21 | Unassigned |
| Ensure `session_id` / `user_id` are passed by upstream tools | WP17b | Auth context not injected consistently across tools | WP2 or WP6 | Unassigned |
| Build tool to assemble individual sections into a full document | WP17b | Section-level generation completed; full document logic not implemented | WP18 | Unassigned |
| Add integration to Google Drive for collaborative editing | WP17b | Drive output interface not yet available | WP20 | Unassigned |
| Define GPT-to-planner trigger mappings (e.g. from user intent to toolchain) | WP17b | User input mappings not yet built for planner mode selection | WP12 or WP16 | Unassigned |
| Add validation layers + templating system for each section type | WP17b | Section types vary; no validation/template logic implemented | WP5 | Unassigned |
| Support document-level workflows: confirmation, approval, versioning | WP17b | Trigger logic and status models not yet implemented | WP6 | Unassigned |
| Token-aware chunking utility (Tiktoken-based) | WP17b | Current chunking is line-based, not token-optimized | WP5 or WP2 | Unassigned |
| Add `chunk_id`, `position` for fine-grained traceability | WP17b | Needed for per-chunk edits and audit logs | WP6 or WP5 | Unassigned |
