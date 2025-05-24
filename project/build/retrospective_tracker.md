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