## ✅ WP16 Tool Testing Results

Tested against: `robust-adventure-production.up.railway.app`

---

### ✅ Tools Verified

| Tool                 | Status   | Notes |
|----------------------|----------|-------|
| uploadTextInput      | ✅ Pass   | Logged input and metadata correctly |
| uploadFileInput      | ✅ Pass   | Extracted and logged file input successfully |
| uploadLinkInput      | ✅ Pass   | Scraped and logged webpage content |
| loadCorpus           | ✅ Pass   | Embedded and stored in Chroma DB (cloud) |
| inputPromptGenerator | ✅ Pass   | Generated structured prompts using dynamic question map |

### ⚠️ Tool Deferred

| Tool          | Status   | Notes |
|---------------|----------|-------|
| inputChecker  | ⚠️ Deferred | No PromptLog entries contain `session_id`, so no target data to check completeness against |

---

### 🛠 Issues Faced + Fixes

1. **Chroma DB not responding**
   - Fix: Switched to local Chroma DB using Docker Compose inside the same Railway project

2. **No logs visible for loadCorpus**
   - Fix: Replaced `print` with `logger` and updated log visibility in Railway

3. **Tool call hangs silently if schema mismatch**
   - Fix: Enhanced validation and exception logging in `api_router.py` and `tool_registry.py`

4. **Chroma server not starting**
   - Fix: Adjusted Docker Compose volumes and port mapping

5. **loadCorpus schema mismatch**
   - Fix: Aligned input payload structure and registry schema definition

---

### 📝 Next Actions

- Consider session ID support for PromptLog to enable `inputChecker`
- Snapshot and trace export (T6b)
- Final UI interface sketch + Completion note

Tested and verified as of: May 22, 2025