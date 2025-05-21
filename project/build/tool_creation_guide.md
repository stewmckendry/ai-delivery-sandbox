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