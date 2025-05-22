## 📌 Scope Update: WP16 PromptLog Metadata Capture

### 🧠 Situation
WP16 is responsible for capturing structured user input aligned to gate artifacts using guided prompts or bulk ingest. These inputs are logged using `log_tool_usage()` into the PromptLog table. However, PromptLog lacks sufficient metadata to trace user input to specific sections of gate documents.

### ✅ Recommendation
Enhance all WP16 tools to include structured metadata in the PromptLog entry. This metadata enables downstream tools like `compose_and_cite` to:
- Retrieve user inputs relevant to a specific gate > artifact > section > intent
- Apply those inputs during document drafting and QA

### ✨ Change in WP16 Scope
**Added Task T6** – "PromptLog Metadata Integration"
- Extend WP16 tools (`inputPromptGenerator`, `inputChecker`) to embed structured metadata block:
```json
"metadata": {
  "gate": 1,
  "artifact": "Budget Memo",
  "section": "Rationale",
  "intent": "justify_budget_rise"
}
```
- Use this in all `log_tool_usage()` calls to enable queryability

### 📊 Impact + Rationale
- Aligns input UX with session memory and drafting tools
- Enables full traceability and validation of user input
- Adds ~1-2h of dev time but avoids future refactors

### 🔭 Anticipated Follow-up
- Recommend WP9 upload tools adopt same metadata convention
- Compose/QA tooling (future WP) will consume these enriched logs

---