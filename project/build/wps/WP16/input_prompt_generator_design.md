### 🧠 Input Prompt Generator – Design Note

**Goal:** Enable dynamic generation of structured input prompts based on selected `gate`, `artifact`, and optional `section`, using metadata defined in `gate_reference_v2.yaml`.

---

### 🔍 Purpose

The `inputPromptGenerator` tool builds question prompts for PolicyGPT to guide user input collection across the various gates and artifacts in the approval process. This replaces static triage maps with a scalable, schema-aligned, metadata-rich system.

---

### 🧩 Components

- **Source File**: `app/tools/tool_wrappers/inputPromptGenerator.py`
- **Prompt Block Schema**: `project/reference/prompt_block_schema.json`
- **Reference Data**: `project/reference/gate_reference_v2.yaml`

---

### ⚙️ How It Works

The tool:
1. Loads `gate_reference_v2.yaml` via GitHub.
2. Locates the correct gate and artifact.
3. For each section, extracts:
   - `section_id`
   - `intents` (used as questions)
   - `mandatory` status
4. For each `intent`, builds a question block with:
   - `question`: The intent string
   - `input_type`: "text" (default)
   - `hints`: From `evaluation_criteria`
   - `metadata`: gate, artifact, section, intent
   - `artifact_*`: Details like purpose, maturity, template path, exemplar path

---

### 📋 Schema Additions

Schema now includes:
- `artifact_name`, `artifact_purpose`
- `artifact_template`, `artifact_exemplar`
- `maturity`, `notes`

These fields help GPT better tailor questions, expectations, and style.

---

### 🌐 Example Usage

```json
{
  "question": "Describe the problem or opportunity.",
  "input_type": "text",
  "answer": null,
  "metadata": {
    "gate": 0,
    "artifact": "investment_proposal_concept",
    "section": "problem_statement",
    "intent": "Describe the problem or opportunity."
  },
  "hints": [
    "Is the problem clearly defined?",
    "Is it aligned with strategic objectives?"
  ],
  "required": true,
  "artifact_name": "Investment Proposal (Concept Case)",
  "artifact_purpose": "Articulate the business problem or opportunity...",
  "artifact_template": "reference/templates/investment_proposal_concept.md",
  "artifact_exemplar": "reference/examples/investment_proposal_concept_gold.md",
  "maturity": "Concept stage...",
  "notes": "PolicyGPT should guide the user..."
}
```

---

### ✅ Status
- Dynamic prompt generation working end-to-end.
- Schema updated and aligned.
- Gate reference enriched with section-level `intents`.

---

### 🔮 Next
- GPT config will use these blocks to guide step-by-step collection.
- Planner will eventually reference these prompts to check completeness and summarize data across sessions.
