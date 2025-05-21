## WP9 Testing Documentation

### ✅ Unit Tests
- `structure_input()` tested independently for timestamp, UUID, truncation logic
- `text_extractor` tested on DOCX, PDF samples
- `retry_ingestion` tested with mocked failures to confirm backoff and retries

### 🧪 Integration Testing
- CLI runner used with real sample inputs:
  - `test_input_samples.txt`
  - PDF sample from Infrastructure Canada site
- Verified output YAML traces written to `logs/ingest_traces/`
- DB records verified via SQL query after ingestion

### 🧪 Manual Schema Validation
- SQLAlchemy introspection used:
```python
from sqlalchemy import inspect
inspect(engine).get_columns('prompt_logs')
```
- Verified fields after `reset_db`

### 🐞 Debugging Aids
- Added print statements in `cli_ingest_runner` to trace failures
- Errors from `pyodbc` often obscure; validated root causes by inspecting SQL manually

### 🚧 Known Gaps
- No automated test coverage yet for `uploadLinkInput` due to dependency on web access
- No Pytest test suite configured (covered manually for now)

### 🔍 Future Recommendations
- Add mocks for external libraries (e.g., newspaper3k)
- Snapshot testing of YAML logs
- Wrap ingestion in a `test_tool_runner.py` fixture

— ProductPod