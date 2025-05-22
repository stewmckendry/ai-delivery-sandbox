## WP16 – Input Prompt UX Layer: Design Overview

### 🎯 Purpose
Design a UX and tooling system that captures user input aligned to gate-specific requirements for PolicyGPT. Supports two modes:
1. **Guided Prompt Mode**: Interactive prompt sequence, inspired by triage-style flows.
2. **Data Dump Mode**: Bulk upload of existing artifacts, parsed and extracted into memory.

### 🧩 System Role in PolicyGPT
The Input Prompt UX Layer serves as the structured intake layer feeding the session memory. It connects gate-specific metadata to downstream document generation logic.

```
User -> [Input Prompt UX Layer] -> [Session Memory / Input Tools] -> [GPT Core: Doc Assembly / Edit / QA]
```

### 📐 Architecture Overview
- **Prompt Generation**: Based on gate type, generates questions using `inputPromptGenerator`
- **Prompt Mode**: Determines flow: step-by-step (guided) vs. ingest all (data dump)
- **Input Tools**: Uses `uploadTextInput`, `uploadFileInput`, `uploadLinkInput` etc. from WP9
- **Input Completeness**: Uses `inputChecker` to validate readiness for doc generation
- **Memory Integration**: Writes all user answers into session memory format

### 🔄 End-to-End Flow (Data View)

1. **Know What to Collect**
   - Load gate metadata from `gate_reference_v2.yaml`
   - Gate metadata defines required fields by intent

2. **User Input Modes**
   - **Guided Prompt**: Calls `inputPromptGenerator` to create prompt sequence
   - **Data Dump**: Uses ingestion tools to process bulk documents

3. **Data Collection**
   - Answers routed via ingestion tools (text, files, links)
   - Stored in session memory model

4. **Validation**
   - `inputChecker` scans memory to flag missing required fields

5. **Use in Generation**
   - Session memory becomes context for GPT-driven document generation

### 🛠 Tool Interfaces
- `inputPromptGenerator` (wrapper tool): Returns prompt spec from gate
- `inputChecker` (wrapper tool): Returns pass/fail + missing intents

### 🧠 Design Decisions
- Reuse triage-style prompt schema (id, intent, mode, type, etc.)
- Schema-driven checker improves validation + reuse
- Wrapper tools match WP3b conventions for tool registration

### 📈 Future Extensions
- Internationalization of prompt wording
- Adaptive prompting based on answers
- Inline feedback on user answer quality

---

Let me know if you want visual diagrams or sequence diagrams added next.