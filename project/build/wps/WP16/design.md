## WP16 – Input Prompt UX Layer: Design Overview (Updated)

### 🎯 Purpose
Design a UX and tooling system that captures user input aligned to gate-specific requirements for PolicyGPT. Supports two modes:
1. **Guided Prompt Mode**: Interactive prompt sequence, inspired by triage-style flows.
2. **Data Dump Mode**: Bulk upload of existing artifacts, parsed and extracted into memory.

### 🧩 System Role in PolicyGPT
The Input Prompt UX Layer serves as the structured intake layer feeding the session memory. It connects gate-specific metadata to downstream document generation logic.

```
User -> [Input Prompt UX Layer] -> [Session Memory / Input Tools] -> [GPT Core: Doc Assembly / Edit / QA]
```

### 🔄 End-to-End Flow (Data View)
1. **Know What to Collect**
   - Load gate metadata from `gate_reference_v2.yaml`
   - Gate metadata defines required fields by intent

2. **User Input Modes**
   - **Guided Prompt**: Uses `inputPromptGenerator` to generate structured questions
   - **Data Dump**: Uses ingestion tools to process uploaded documents

3. **Data Collection + Storage**
   - All input tools (WP16 or WP9) call `log_tool_usage()` → writes to PromptLog
   - WP16 tools will enrich these calls with `metadata` including `gate`, `artifact`, `section`, `intent`

4. **Validation + Memory Trace**
   - `inputChecker` validates completeness
   - Session snapshot may include structured summary for rehydration

5. **Downstream Use**
   - Compose tool can query PromptLog entries by section/intent
   - Enables drafting logic by filtering structured input context

### 🧠 Change Introduced in WP16
- Extend WP16 tools to include structured `metadata` in PromptLog calls
- Define a metadata schema to align `user input` with `gate -> artifact -> section -> intent`
- Recommend aligning WP9 upload tools next

### ✅ Implementation Change
- Modify all WP16 tools to add metadata block
- Update schema spec to include:
```json
"metadata": {
  "gate": 1,
  "artifact": "Budget Memo",
  "section": "Rationale",
  "intent": "justify_budget_rise"
}
```
- This will live inside `log_tool_usage()` entries

### 📈 Benefits
- Enables downstream drafting by context
- Backwards-compatible with existing PromptLog
- Avoids tight coupling to future compose tool

---