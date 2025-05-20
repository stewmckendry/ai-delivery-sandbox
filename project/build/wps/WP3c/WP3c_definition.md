## WP ID: WP3c
## WP Name: Middleware + Logging

### 🌟 Outcome
By the end of this WP, as a **toolchain middleware layer**, I will be able to intercept, log, and augment tool executions across PolicyGPT. This enables observability, resilience, and advanced behaviors such as fallback logic and internal knowledge lookups.

### 🯽 Scope
**In Scope:**
- Middleware for toolchain operations
- Logging tool usage and failures
- Tool wrappers for context enhancement
- Internal KB search and commit tools

**Out of Scope:**
- External web search (future WP14)
- Planner breakdown or rehydration (WP3a)
- Evidence citation and user-facing tooling (WP8)

### 📦 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/engines/error_middleware.py` | Captures and logs tool errors; supports retries/fallback. |
| `app/engines/toolchain_middleware.py` | Wraps tools to inject metadata, memory, and observability. |
| `app/tools/search_knowledge_base.py` | Looks up content from an internal KB based on tool inputs. |
| `app/tools/push_commit.py` | Commits final tool outputs or intermediate results to long-term store. |
| `app/db/models/ErrorLog.py` | Logs toolchain and runtime errors with trace context. |
| `app/db/models/ToolLog.py` | Captures tool invocation metadata and outputs. |
| `app/db/models/ExternalServiceLog.py` | Logs 3rd party service calls (e.g., Drive, APIs). |
| `app/db/models/FallbackUsageLog.py` | Records fallback attempts and success rates. |
| `.env.sample` | Environment variable template for services, keys, and DB config. |

### 📄 Supporting Documentation (to generate)
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WP3c/WP3c_middleware_design.md` | Middleware intercept logic, retry flows, logging schema. |
| `project/build/wps/WP3c/WP3c_kb_stub_notes.md` | MVP plan for knowledge base stub (e.g., FAISS or static lookup). |
| `project/build/wps/WP3c/WP3c_test_matrix.md` | Edge cases, log scenarios, and tool invocation test flows. |

### ✅ Acceptance Criteria
- [ ] All tool invocations pass through toolchain middleware
- [ ] Errors are logged to `ErrorLog`
- [ ] Tool calls and responses captured in `ToolLog`
- [ ] KB search is callable and returns mock/stubbed content
- [ ] Commit tool operational with persistent outputs

### 🛠 Tasks
| Task ID | Description |
|---------|-------------|
| T1 | Design logging and middleware architecture |
| T2 | Implement `toolchain_middleware.py` to wrap all tools |
| T3 | Implement `error_middleware.py` for error capture + retry hooks |
| T4 | Implement `ToolLog.py`, `ErrorLog.py`, and supporting models |
| T5 | Build `search_knowledge_base.py` with stubbed index backend |
| T6 | Implement `push_commit.py` and trace persistence |
| T7 | Write `.env.sample` for local development configs |

### 📚 Reference Documentation
| File Path | Usage |
|-----------|--------|
| `session_memory_model_v2.md` | Describes logging targets and fallback needs |
| `tool_catalog_v2.md` | Tool wrappers and middleware roles |
| `api_contracts_v2.md` | Expected inputs/outputs for KB search and commit tools |
| `error_handling_matrix_v2.md` | Retry and fallback rules |
| `system_architecture_v2.md` | Middleware integration points and flows |

### 📝 Notes to Development Team
- KB search is stubbed for MVP, full vector DB optional later
- This WP focuses on backend enablement, not UI integration
- Middleware should support logging for live and replayed flows

---

### 🔍 Clarifications

**Q: Is `search_knowledge_base` fully implemented here?**
**A:** Yes, a stub or MVP version is implemented in this WP to support internal tool use. Full citation logic and user flows are deferred to WP8.

**Q: What knowledge base is used?**
**A:** MVP assumes a simple document index or local embedding search (e.g., FAISS). Later WPs may evolve this.

**Q: When is KB search exposed to end users?**
**A:** In WP8, when citation tools are built to leverage this lookup.

**Q: Where is external web search scoped?**
**A:** This is deferred to a new proposed WP14: "External Source Integration".