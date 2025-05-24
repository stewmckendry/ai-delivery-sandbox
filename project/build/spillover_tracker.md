| Item | Source WP | Reason for Deferral | Suggested Owner | Status |
|------|-----------|----------------------|------------------|--------|
| Implement `queryCorpus` for embedding search + memory recall | WP17b | Required for memory lookup; deferred due to tool not being built yet | WP21 | Unassigned |
| Ensure `session_id` / `user_id` are passed by upstream tools | WP17b | Auth context not injected consistently across tools | WP2 or WP6 | Unassigned |
| Build tool to assemble individual sections into a full document | WP17b | Section-level generation completed; full document logic not implemented | WP18 | Unassigned |
| Add integration to Google Drive for collaborative editing | WP17b | Drive output interface not yet available | WP20 | Unassigned |
| Define GPT-to-planner trigger mappings (e.g. from user intent to toolchain) | WP17b | User input mappings not yet built for planner mode selection | WP12 or WP16 | Unassigned |
| Add validation layers + templating system for each section type | WP17b | Section types vary; no validation/template logic implemented | WP5 | Unassigned |
| Support document-level workflows: confirmation, approval, versioning | WP17b | Trigger logic and status models not yet implemented | WP6 | Unassigned |
| Token-aware chunking utility (Tiktoken-based) | WP17b | Current chunking is line-based, not token-optimized | WP5 or WP2 | Unassigned |
| Add `chunk_id`, `position` for fine-grained traceability | WP17b | Needed for per-chunk edits and audit logs | WP6 or WP5 | Unassigned |
| Improve input validation with `parse_obj_as()` | WP18 | Validation upgrades introduced mid-build | WP5 | Unassigned |
| Auto-validate registry and manifest alignment | WP18 | Tool registry drifted from implementation | WP3b | Unassigned |
| Expand artifact schema documentation | WP18 | Onboarding for new devs was hindered by unclear schema | WP1b or WP12 | Unassigned |
| Adopt snapshot-based unit testing | WP18 | Existing tests missed regressions in rendering output | WP5 | Unassigned |
| Drive upload integration | WP18 | Placeholder only; actual Drive service not wired | WP20 | Unassigned |
| GPT interface toolchain invocation + chunk-safe rendering | WP18 | Not integrated with GPT UX layer; chunk limits need handling | WP16 or WP12 | Unassigned |
| View/download final docs via UX and CLI | WP18 | No UI or CLI endpoint yet for output access | WP6 or WP16 | Unassigned |
| CI test suite for full toolchain validation | WP18 | Tests are local/manual; CI workflow missing | WP3c or WP5 | Unassigned |
| Add support for DOCX upload/output | WP20 | Requested for Drive compatibility; not yet implemented | WP10 or WP20 | Unassigned |
| Support preview fetch (not just PDF) | WP20 | Drive fetch only returns PDF; preview UX not wired | WP20 | Unassigned |
| Add `project_id` to Drive folder routing | WP20 | Needed for multi-project support and traceability | WP20 | Unassigned |
| Permission-based Drive sharing | WP20 | Access control not implemented | WP20 | Unassigned |
| Auto-diff support between Drive version and draft | WP20 | No logic yet to compare Drive output and revised drafts | WP5 or WP11 | Unassigned |
| UI integration with upload/download links | WP20 | Needs hooks into GPT + front-end for usability | WP16 | Unassigned |