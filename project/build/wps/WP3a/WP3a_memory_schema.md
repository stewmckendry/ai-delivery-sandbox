# WP3a Memory Schema Notes

## 🧠 PromptLog
Tracks individual tool runs, GPT calls, or user interactions.

| Field | Type | Description |
|-------|------|-------------|
| id | int | Primary key |
| timestamp | datetime | UTC timestamp of log |
| tool | str | Tool name invoked |
| input_summary | str | Hash or short text of input |
| output_summary | str | Hash or short text of output |
| full_input_path | str | Path or URI to full input file |
| full_output_path | str | Path or URI to full output file |
| user_id | str | Optional user reference |
| session_id | str | Optional session reference |

## 📦 SessionSnapshot
Persists state to resume planner execution.

| Field | Type | Description |
|-------|------|-------------|
| id | int | Primary key |
| timestamp | datetime | UTC timestamp of snapshot |
| session_id | str | Session identifier (e.g. run ID) |
| snapshot_path | str | Path to session JSON file |
| notes | str | Optional notes or tags |
| user_id | str | Optional user ID |

## 📁 Storage Notes
- JSONL logs go to `logs/prompt_logs.jsonl`
- Session snapshots go to `logs/session_snapshots/`
- In production: DB logs + file paths reference GitHub or blob store

## 🔄 Replay Support
- Planner can replay a run using trace and logs
- `load_latest_snapshot()` used for last-known good state

## 🔐 Trace Fields (YAML)
```yaml
reasoning_trace:
  task_id: generate-section
  planner_decisions:
    - step: 0
      tool: intent_classifier
      input: ...
      output: ...
    - step: 1
      tool: schema_loader
      ...
```