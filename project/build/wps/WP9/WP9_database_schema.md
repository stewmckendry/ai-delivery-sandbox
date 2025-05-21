## Database Schema and Handlers (WP9)

### 📋 Tables

#### `prompt_logs`
Stores tool usage logs for traceability and analytics.
- `id` (UUID, PK)
- `tool` (str): Name of the tool used
- `input_summary` (str)
- `output_summary` (str)
- `full_input_path` (str)
- `full_output_path` (str)
- `session_id` (str, nullable)
- `user_id` (str, nullable)
- `timestamp` (datetime)

#### `session_snapshots`
Captures memory state for handoff or recall.
- `snapshot_id` (str, PK)
- `session_id` (str)
- `path` (str): YAML path of snapshot
- `created_at` (datetime)

### ⚙️ Handlers

#### `log_tool_usage(...)` (in `memory_sync.py`)
- Writes to `PromptLog`
- Logs YAML and DB in one call
- Optional fields: session_id, user_id, full paths

#### `SessionSnapshot` creation
- See `createSessionSnapshot.py`
- Instantiates a DB model and adds via SQLAlchemy session

### 🧪 Schema Verification
To check current schema:
```python
from sqlalchemy import inspect
inspect(engine).get_columns('prompt_logs')
```

To reset DB locally:
```python
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
```

### 🔁 Sync Advice
- Keep `structure_input`, DB models, and `to_dict()` aligned
- Confirm default timestamps, UUIDs, and nullable fields are consistent

— ProductPod