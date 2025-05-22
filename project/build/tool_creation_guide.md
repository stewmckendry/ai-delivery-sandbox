# Guide: Creating New Tools in the AI Delivery Framework

This guide is for WP Pods implementing new tools using the `tool_registry` and `toolchain` system.

## 📘 Recommended Reading
- `tool_registry_system.md`
- `WP3a_toolchain_system.md`

## 🧩 Components to Update
1. **Define your tool metadata**:
   - Add entry in `project/system_design/tool_catalog.yaml`
   - Specify `tool_id`, input/output schema, and routes

2. **Create Tool Wrapper**:
   - Use existing examples (`uploadTextInput`, etc.) in `app/tools/tool_wrappers`
   - Follow base class structure (`Tool`) and override `run_tool`

3. **Update Tool Metadata JSON (if needed)**:
   - Ensure the metadata reflects parameters like `tool_name`, `input_type`, etc.

4. **Log Output Using memory_sync.py**:
   - Use `log_tool_usage()` to write to `PromptLog` and optionally generate `SessionSnapshot`
   - Be consistent with the `structure_input()` format

5. **Local Testing (CLI)**:
   ```bash
   python3 -m app.tools.tool_wrappers.cli_ingest_runner <your_input> --type <your_tool_id>
   ```

6. **Cloud Testing (API)**:
   ```bash
   curl -X POST https://<your-deployment-url>/tools/<your_tool_id> \
     -H "Content-Type: application/json" \
     -d '{"text": "example input"}'
   ```

## Testing New Tools (Guide for WP Pods)

When creating a new tool:
1. Validate CLI tests with realistic input examples.
2. Add `curl` commands to test cloud deployments.
3. Ensure schema validation catches missing/invalid fields.
4. Avoid local file writes in cloud—use `is_cloud_env()` to skip.
5. Output a structured result and confirm DB logs are written.


## Memory Logging System Overview

### 📘 PromptLog
- **Purpose:** Tracks each tool invocation.
- **Fields:** Tool, input/output summaries, file paths, session/user IDs.
- **Storage:** 
  - Writes JSON line to `prompt_logs.jsonl` (local, if not cloud).
  - Persists structured record in SQL DB (PromptLog table).

### 📙 SessionSnapshot
- **Purpose:** Captures session history at a point in time.
- **Fields:** Snapshot ID, session ID, file path, timestamp.
- **Storage:**
  - Writes `.yaml` or `.json` to `snapshots/` (if not cloud).
  - Persists reference in SQL DB (SessionSnapshot table).

### 🔗 Integration in Tools
Each tool (e.g., `uploadFileInput`) logs usage:
```python
entry = structure_input(raw, source, tool_name="uploadFileInput")
out_path = write_trace(entry)
log_tool_usage(tool_name, input_summary, output_summary, out_path, ...)
```

For snapshots:
```python
entries = [e.to_dict() for e in PromptLog.query.all()]
if not is_cloud_env():
    write snapshot to disk
log snapshot in SessionSnapshot DB
```

## ✅ Best Practices
- Start from an existing tool wrapper for structure
- Keep tool names consistent across file, metadata, and DB
- Ensure `structure_input()` aligns with DB model
- Handle local vs. cloud YAML logging appropriately

## ❌ Common Pitfalls
- Forgetting to add tool entry to `tool_catalog.yaml`
- Missing metadata mismatches in DB logging
- `structure_input()` returning keys not present in `PromptLog`
- Writing YAML logs in environments (e.g., Railway) that don’t support local file I/O

---

For questions or to propose improvements to the registry/toolchain design, tag WP12.