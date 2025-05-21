# 🧰 WP3a Toolchain System Overview

## 📌 Purpose
This doc explains how the PolicyGPT planner invokes toolchains — ordered sets of tools that execute tasks like drafting or refining gate documents.

## ⚙️ Key Components

### 1. **PlannerOrchestrator**
Located at: `app/engines/planner_orchestrator.py`
- Entry point for planner execution
- Accepts `intent` and `inputs`
- Looks up the toolchain for that intent
- Executes tools in order, passing state between them
- Supports `live` and `replay` mode
- Logs outputs and builds `reasoning_trace`

### 2. **Tool Catalog**
Located at: `app/tools/__init__.py`
- Maps tool names (strings) to callable tool objects
- Stubs used for WP3a; real implementations expected in WP3b

### 3. **Tool Invocation Pattern**
Each tool must expose a `.run(input_data)` method.
Output of one is input to the next.
Planner also logs I/O at each step via `log_tool_usage()`

### 4. **Memory + Logs**
- `memory_sync.py`: Handles `log_tool_usage`, `save_session_snapshot`, `load_latest_snapshot`
- Prompt logs: `logs/prompt_logs.jsonl`
- Snapshots: `logs/session_snapshots/*.json`

### 5. **Replay Mode**
- Replays a prior planner run using only logs and snapshot
- No tool execution occurs
- Useful for debug, analysis, compliance

## 📐 Example Flow
```python
planner.run("generate_section", {"section": "outputs"})
```
Toolchain:
1. `intent_classifier`
2. `schema_loader`
3. `section_writer`

Output includes final results + YAML reasoning trace.

## 🧪 Test Coverage
See: [`WP3a_test_cases.md`](./WP3a_test_cases.md)

## 📤 Future Expansion
- Toolchains will be made dynamic (via config or YAML)
- DB integration via WP4
- Tools wired with GPT + system integrations in WP3b