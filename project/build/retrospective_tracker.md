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