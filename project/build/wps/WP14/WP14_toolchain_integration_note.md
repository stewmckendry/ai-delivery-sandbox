## WP14 Toolchain Integration Note

### Tool: `webSearch`

**Path:** `app/tools/tool_wrappers/web_search.py`
**Type:** Planner-invoked tool with `Tool` class pattern
**Registered As:** `webSearch` in `tool_catalog.yaml`

### Inputs (via planner):
```json
{
  "query": "string",
  "search_type": "general | jurisdiction | market",
  "context": { "project_profile": { ... }, ... }
}
```

### Output Format:
List of normalized entries:
```json
[
  {
    "title": "...",
    "snippet": "...",
    "source": "...",
    "date": "...",
    "url": "..."
  },
  ...
]
```

### Planner Routing
- Triggered via `intent: external_web_search`
- Routed in `planner_orchestrator.py`
- Called as fallback in `generate_section_chain.py` when memory is empty

### Downstream Compatibility
- Output format is consumable by `section_synthesizer`
- Result summaries are also logged to `PromptLog` and `ReasoningTrace`

### Logging
- Each search writes to `WebSearchLog` with:
  - `search_type`, `query`, `tool_invoked_by`
  - `user_id`, `session_id`, `project_id`, `timestamp`

### Notes
- Supports modular handlers by `search_type`
- Prompts are stored in `search_prompts.yaml`
- Live queries powered by Bing via RapidAPI