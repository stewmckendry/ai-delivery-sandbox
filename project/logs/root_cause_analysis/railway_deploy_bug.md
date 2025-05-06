## 🐞 Root Cause Analysis – Railway Deployment Failures

### 🧭 Context
The initial deployment of the CareerCoach FastAPI app to Railway failed due to a series of uncaught integration, dependency, and import issues. These blocked the app from starting and executing requests.

---

### 🚨 Symptoms Observed
1. `ModuleNotFoundError` for `schemas` and other internal modules
2. `ImportError` for undefined classes like `NotionClient`, `AirtableClient`, `SegmentClient`
3. `ModuleNotFoundError` for external libraries: `httpx`, `yaml`
4. Failure to locate the FastAPI app instance due to missing or misreferenced `main.py`

---

### 🔍 Root Causes
| Category | Root Cause | Resolution |
|----------|------------|------------|
| ✅ Imports | Relative imports like `from ..schemas` failed in Railway’s execution context | Replaced with absolute imports using `project.app.*` |
| ❌ Missing Definitions | `NotionClient`, `AirtableClient`, `SegmentClient` were not defined | Replaced with actual available functions (e.g. `save_to_notion`, `get_reflections`) |
| 📦 Dependencies | `httpx` and `pyyaml` were used but missing from `requirements.txt` | Added them explicitly with proper versioning |
| 🚀 Entrypoint | No `main.py` or app object was defined in accessible path | Created `project/app/main.py` to wire routes and expose `app = FastAPI()` |
| 📄 Segment Route | Route used a nonexistent client instead of YAML loader | Rewired to `yaml_loader.load_segment(category)` with proper path |

---

### ✅ Actions Taken
- Fixed all broken or missing imports
- Stubbed undefined references or routed to proper modules
- Added `main.py` and start command
- Updated `requirements.txt`
- Rewrote segment route handler
- Refactored prompt and memory handlers

---

### 🧠 Lessons Learned
- Always fetch and review route modules before deployment
- Don’t assume client wrappers exist—verify or stub
- Validate start commands and module paths for FastAPI
- Require external deps to be listed in `requirements.txt`
- Routes should match documented design (specs vs. impl gap)

---

### 📌 Recommendation
Add pre-deploy checklist:
- [ ] Validate route imports resolve
- [ ] Check `main.py` path exists and exposes `app`
- [ ] Confirm all expected dependencies are listed
- [ ] Ensure segment and prompt handlers map to spec

App is now successfully deployed and endpoints are stable.