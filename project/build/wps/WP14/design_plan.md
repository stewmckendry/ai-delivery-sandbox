## WP14 Design Plan: External Search Tool for Artifact Drafting

### Goal
Develop a modular external search tool integrated with the PolicyGPT planner and toolchain to support evidence gathering from public sources. This tool must support multiple search types, normalize results, and ensure traceability through logging.

### Components & Architecture

#### 1. `web_search.py` (Search Executor)
- Calls web APIs or public search engines based on type.
- Routes to search handlers (e.g., general, market, jurisdiction).

#### 2. `search_handlers/<type>.py`
- Specialized logic per search type.
- Examples: `general.py`, `jurisdiction.py`, `market.py`
- Encapsulate query logic, filters, and parsing rules.

#### 3. `web_search_formatter.py`
- Converts raw search results into normalized format:
  ```yaml
  - title: <>
    snippet: <>
    source: <>
    date: <>
    url: <>
  ```
- Ensures compatibility with `section_synthesizer` and planner tools.

#### 4. `web_search_logger.py`
- Logs query, search type, timestamp, user/session metadata, and result quality indicators.
- Writes to new `WebSearchLog` DB model.

#### 5. `WebSearchLog.py`
- Captures:
  - `search_type`
  - `query`
  - `results_summary`
  - `tool_invoked_by`
  - `user_id`, `session_id`
  - `timestamp`

#### 6. `search_prompts.yaml`
- YAML with prompt templates by search type
- Example: academic tone for policy scans vs commercial scan phrasing

#### 7. Integration
- Tool registered in `tool_catalog.yaml`
- Planner route added in `planner_orchestrator.py` under `external_web_search` intent
- Invocation from `generate_section_chain.py` as fallback after KB search

#### 8. Logging
- All search runs log to `PromptLog`
- Result summaries saved in trace for `ReasoningTrace`

### Design Principles
- **Extensibility**: Add new `search_type` handlers without changing core logic
- **Reliability**: Rate limit API usage and handle failures gracefully
- **Traceability**: Full log of every search and its context