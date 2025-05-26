## WP ID: WP14
## WP Name: External Source Integration

### 🌟 Outcome
By the end of this WP, as a **policy drafter**, I will be able to search and retrieve relevant information from trusted public web sources or APIs in real time. This capability enhances the breadth and freshness of evidence used in policy documents, ensuring relevance and credibility.

### 🧽 Scope
**In Scope:**
- Querying public search engines or trusted APIs from within toolchain
- Normalizing and structuring external content for planner/tool consumption
- Logging search activities, results, and context metadata
- Provide `web_search` as an optional tool step in `generate_section_chain` (e.g., insert after `memory_retrieve`)
- Output should be formatted for compatibility with `section_synthesizer` inputs (text string or bullet list)
- Allow search to be scoped by metadata (e.g., `gate`, `artifact`, `section`, `intent`) provided by planner

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
| `app/engines/toolchains/generate_section_chain.py` | Updated toolchain to optionally include `web_search` |
| `app/tools/tool_wrappers/web_search.py` | Wrapper class for planner/toolchain integration (Tool class format) |
| `project/reference/gpt_tools_manifest.json` | Register `web_search` for GPT callability |


### 📄 Supporting Documentation (to generate)
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WP14/WP14_search_tool_flow.md` | Flow diagram of search execution, formatting, and logging |
| `project/build/wps/WP14/WP14_example_queries.md` | Illustrative queries and structured responses examples |
| `project/build/WPs/WP14/WP14_toolchain_integration_note.md` | How to register and invoke `web_search` in planner context |
| `project/docs/guides/using_web_search.md` | Guide for GPT or devs on triggering and interpreting search tool output |

### 🔁 Toolchain Integration – Clarification
Search results should:
- Be added to `input_dict` as `external_evidence` for `section_synthesizer`
- Be included in `prompt_used` trace for reasoning transparency
- Be logged in `PromptLog` with the `web_search` tool label
- Include fallback/empty behavior if no results returned

### ✅ Acceptance Criteria
- [ ] `web_search.py` integrates with planner toolchain and external endpoints
- [ ] Results are formatted consistently for downstream tools
- [ ] All search activities are logged in `WebSearchLog`
- [ ] Search usage is verifiable for audit and transparency

### 💪 Tasks
| Task ID | Description |
|---------|-------------|
| T1 | Implement `web_search.py` using Tool class for planner + GPT compatibility |
| T2 | Normalize output with `web_search_formatter.py` to produce structured string or list for prompts |
| T3 | Build logger and `WebSearchLog.py` DB model to track tool usage, timestamps, and metadata |
| T4 | Add `web_search` to `generate_section_chain.py` and update `planner_orchestrator.py` intent mapping |
| T5 | Register tool in `tool_catalog.yaml` and `gpt_tools_manifest.json` |
| T6 | Write CLI integration test in `test_web_search_toolchain.py` and validate output chaining |
| T7 | Create documentation: flow diagrams, example queries, toolchain integration notes |
| T8 | Add search-related reasoning and output fields to `ReasoningTrace` (optional `external_evidence`) |


### 📚 Reference Documentation
| File Path | Usage |
|-----------|--------|
| `tool_catalog_v3.md` | Describes search tools, inputs/outputs, logging expectations |
| `session_memory_model_v2.md` | Describes how external results can feed mid-term memory and tool plans |
| `generate_section_chain.py` | Current toolchain to which `web_search` will be added |
| `section_synthesizer.py` | Tool that will consume structured search output |
| `memory_sync.py` | Pattern for saving reasoning and tool usage trace |
| `section_draft_output.py` | Schema design to validate downstream outputs |
| `PromptLog.py`, `ReasoningTrace.py` | Tool logging and structured trace format |
| `planner_orchestrator.py` | Planner routing by `intent` and toolchain declaration |
| `tool_catalog.yaml`, `gpt_tools_manifest.json` | Tool registration for GPT + planner invocation |

### 📝 Notes to Development Team
- Ensure search results are cached or rate-limited to avoid API abuse
- Format all outputs for compatibility with `evidence_lookup` or planner consumption
- Log sufficient metadata to enable future tuning of search prompts

### 🧠 Clarifications
- 🤖 **Planner Integration:** Search tool will be invoked by planner during research-heavy drafting tasks
- 🔐 **Security Note:** Ensure only whitelisted APIs or public sources are accessed
- 💡 **Post-processing:** Output should be structured to allow re-use in citation or evidence tools
- Trace tool inputs/output to gate, artifact, and section
- Use structured output formats compatible with downstream prompt usage
- Ensure external content is logged, verifiable, and reusable