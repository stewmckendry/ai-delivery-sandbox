## PromptLog Metadata Enhancement Design

### Purpose
Enable structured metadata capture for user inputs logged via tools in PromptLog to support downstream processing and document generation.

### Target
Update `PromptLog` table to add a `metadata` column (type: `JSON`) to store contextual fields:

```json
{
  "gate": 0,
  "artifact": "investment_proposal_concept",
  "section": "problem_statement",
  "intent": "define_problem"
}
```

### Source of Metadata
- **Tools** (e.g., `uploadTextInput`, `uploadFileInput`) via optional `metadata` parameter in tool inputs.
- **GPT** or front-end generates `intent` as part of tool invocation.

### Benefits
- Enables traceability of input purpose and context.
- Powers downstream tools like `compose_and_cite`, `inputChecker`, and review interface.
- Allows for filtering, reviewing, and reusing structured input.

### Implementation Steps
- Patch `PromptLog` to add `metadata` field.
- Update ingestion and trace logging utilities.
- Modify tools to propagate metadata.
- Add test coverage.
- Notify Pod Lead and downstream Pods.

### Risks
- Ensuring all tools consistently pass metadata.
- Potential schema migration required in production DB.

### Status
- ✅ Design committed
- ⏳ Implementation next steps tracked in WP16 `task_list.md`