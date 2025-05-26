### WP14 Retrospective

#### 💪 What Went Well
- Web search worked well with SerpAPI after pivot from RapidAPI.
- Search tool integration into toolchain was clean and modular.
- Reasoning trace and section generation showed high-quality synthesis.
- Full E2E test coverage validated real usage flows.

#### 🤕 What Was Hard
- RapidAPI services (Bing, ContextualWeb) failed unexpectedly.
- YAML indentation error in `tool_catalog.yaml` was hard to detect.
- Tool registry fallback logic needed improvements for transparency.
- Minor `.env` and SQL setup hurdles took time to unblock.

#### 🧠 Lessons Learned
- Always verify service URLs directly in browser or Postman.
- Add extra logging for dynamic tool loading to avoid silent fails.
- Schema-first thinking helped enforce output shape consistency.

#### 🔁 Iteration Improvements
- Added `web_search` to `generate_section_chain` via modular tooling.
- Gracefully merged multiple memory types in `section_synthesizer`.
- Tool registry logs raw and loaded tool keys for better debugging.
- Simplified table creation for `WebSearchLog` to unblock deployment.

#### 📌 Takeaways
- External search enhances section quality — should be used routinely.
- Logging search results enables future caching, analytics, and reuse.
- Project is now better equipped for mixed internal + external knowledge.

---

✅ **WP14 successfully delivered and validated.**