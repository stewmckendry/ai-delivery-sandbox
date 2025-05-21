## WP1a Test Plan – Scaffolding & Assembly

### 🧪 Unit Tests

#### ✅ `gate_section_scaffolder.py`
- Parses gate_id + artifact_id from YAML
- Outputs JSON with correct section count
- Includes required fields: `section_id`, `title`, `next_pod_hint`

#### ✅ `gate_section_expander.py`
- Reads scaffold file
- Returns expanded sections (mocked)
- Propagates `title`, `section_id`, and replaces content

#### ✅ `final_document_assembler.py`
- Combines sections in order
- Writes `.md` and `.json` correctly
- Includes metadata in header and gateblock

---

### 🔁 Integration Test: End-to-End Pipeline

#### Test: `gate_01` + `business_case`
Steps:
1. Run scaffolder → save `scaffold.json`
2. Run expander → save `expanded.json`
3. Run assembler → check markdown and gateblock output

**Checks:**
- `.md` includes section titles and generated text
- `.json` contains matching section structure

---

### 📐 Output Format Validation
- `.md` is markdown-valid with heading structure
- `.json` validates against gateblock schema stub:
```json
{
  "doc_id": "string",
  "gate_id": "string",
  "artifact_id": "string",
  "sections": [
    { "section_id": "string", "title": "string", "content": "string" }
  ]
}
```

---

Prepared by: `WP1aPod`