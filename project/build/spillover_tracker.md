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