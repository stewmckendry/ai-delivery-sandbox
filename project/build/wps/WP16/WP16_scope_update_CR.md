## 📌 Scope Update: WP16 PromptLog Metadata Capture (Revised)

### 🧠 Situation
WP16 is responsible for capturing structured user input aligned to gate artifacts using guided prompts or bulk ingest. These inputs are logged using `log_tool_usage()` into the PromptLog table. However, PromptLog lacks sufficient metadata to trace user input to specific sections of gate documents.

### ✅ Recommendation
Enhance core input ingestion tools (from WP9) to include structured metadata in the PromptLog entry. This metadata enables downstream tools like `compose_and_cite` to:
- Retrieve user inputs relevant to a specific gate > artifact > section > intent
- Apply those inputs during document drafting and QA

### ✨ Change in WP16 Scope
**Added Task T6** – "Patch Upload Tools with Metadata"
- Extend WP9 tools (`uploadTextInput.py`, `uploadFileInput.py`, `uploadLinkInput.py`) to embed structured metadata block:
```json
"metadata": {
  "gate": 1,
  "artifact": "Budget Memo",
  "section": "Rationale",
  "intent": "justify_budget_rise"
}
```
- Pass this into `log_tool_usage()` to enable queryability

### 📊 Impact + Rationale
- Enables downstream drafting by context
- Backwards-compatible with existing PromptLog
- Avoids tight coupling to future compose tool
- Adds ~2h effort to WP16, offsets future rework

### 🔭 Clarification
No metadata updates will be added to `inputPromptGenerator` or `inputChecker`, as these do not handle user inputs.

---