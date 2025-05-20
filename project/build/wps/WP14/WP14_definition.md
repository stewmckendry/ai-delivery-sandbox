## WP ID: WP14
## WP Name: External Source Integration

### 🌟 Outcome
By the end of this WP, as a **policy drafter**, I will be able to search and retrieve relevant information from trusted public web sources or APIs in real time. This capability enhances the breadth and freshness of evidence used in policy documents, ensuring relevance and credibility.

### 🧽 Scope
**In Scope:**
- Querying public search engines or trusted APIs from within toolchain
- Normalizing and structuring external content for planner/tool consumption
- Logging search activities, results, and context metadata

**Out of Scope:**
- Evidence validation or citation (WP8)
- Internal document retrieval or search (handled in WP3c)
- UI interface for search queries (future UI WP)

### 📦 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/tools/web_search.py` | Executes queries against public search engines or APIs |
| `app/tools/web_search_formatter.py` | Standardizes output into structured format |
| `app/tools/web_search_logger.py` | Logs query parameters, timestamp, and response metadata |
| `app/db/models/WebSearchLog.py` | DB model capturing search event history and usage context |

### 📄 Supporting Documentation (to generate)
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WP14/WP14_search_tool_flow.md` | Flow diagram of search execution, formatting, and logging |
| `project/build/wps/WP14/WP14_example_queries.md` | Illustrative queries and structured responses examples |

### ✅ Acceptance Criteria
- [ ] `web_search.py` integrates with planner toolchain and external endpoints
- [ ] Results are formatted consistently for downstream tools
- [ ] All search activities are logged in `WebSearchLog`
- [ ] Search usage is verifiable for audit and transparency

### 💪 Tasks
| Task ID | Description |
|---------|-------------|
| T1 | Implement `web_search.py` for API and search engine integration |
| T2 | Normalize output with `web_search_formatter.py` |
| T3 | Build logger and DB model for search tracking |
| T4 | Write toolchain integration tests and verify planner routing |
| T5 | Document search flow and output templates |

### 📚 Reference Documentation
| File Path | Usage |
|-----------|--------|
| `tool_catalog_v2.md` | Describes search tools, inputs/outputs, logging expectations |
| `session_memory_model_v2.md` | Describes how external results can feed mid-term memory and tool plans |

### 📝 Notes to Development Team
- Ensure search results are cached or rate-limited to avoid API abuse
- Format all outputs for compatibility with `evidence_lookup` or planner consumption
- Log sufficient metadata to enable future tuning of search prompts

### 🧠 Clarifications
- 🤖 **Planner Integration:** Search tool will be invoked by planner during research-heavy drafting tasks
- 🔐 **Security Note:** Ensure only whitelisted APIs or public sources are accessed
- 💡 **Post-processing:** Output should be structured to allow re-use in citation or evidence tools