## WP14 Impact Assessment: Migrating from RapidAPI to SerpAPI

This document summarizes required changes to switch from Bing via RapidAPI to SerpAPI for external web search.

---

### 🔍 Summary
| Component | Impact | Fix Required |
|----------|--------|---------------|
| `search_api_utils.py` | ✅ Major | Replace Bing API logic with SerpAPI logic and format |
| `web_search_formatter.py` | ✅ Minor | Confirm field compatibility (title, url, snippet, date) |
| `web_search_logger.py` | ❌ None | No API-specific changes |
| `web_search.py` | ❌ None | No changes if handler return values match spec |
| `general.py`, `jurisdiction.py`, `market.py` | ❌ None | No change unless API query struct differs dramatically |
| `planner_orchestrator.py`, `generate_section_chain.py` | ❌ None | Planner logic is unchanged (calls tool wrapper) |
| `WebSearchLog.py` | ❌ None | Logging schema remains unchanged |

---

### 🛠️ Required Fix Summary
- ✅ Replace all of `bing_web_search()` in `search_api_utils.py`
- ✅ Validate field names in `web_search_formatter.py` match SerpAPI output:
  - `title`, `snippet`, `url`, `source`, `date`
- ❌ All other components can remain unchanged (tool interface is stable)

---

### 📁 Files Affected
- `app/tools/tool_utils/search_api_utils.py`
- `app/tools/tool_utils/web_search_formatter.py`

Estimated effort: **Low** — scoped to a single utility function and formatting check