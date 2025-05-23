# 🧱 WP17b – Chunking & Output Schema Validation

## 📌 Overview
This note documents two enhancements to the `generate_section` toolchain:
- **Output Schema Validation** using Pydantic
- **Chunking of Draft Text** for traceability and downstream processing

---

## 🧪 Output Schema Validation

### What It Is
Schema validation enforces structure on tool outputs using a Pydantic model. It ensures the expected fields are always present and correctly typed.

### Why We're Doing It
- Ensures reliability across toolchain steps
- Allows early error detection and schema migration
- Enables clear input/output contracts for other Pods

### How We Implemented It
- Created `SectionDraftOutput` schema in `app/schemas/section_draft_output.py`
- Used in `section_synthesizer.py` and `section_refiner.py` to wrap return values
- Returns `dict()` for serialization

### How to Reuse
- Import the schema in any tool wrapper: `from app.schemas.section_draft_output import SectionDraftOutput`
- Validate output before returning from `run_tool()`

### Future Enhancements
- Schema registry per tool
- Version control for schema evolution
- Field-level confidence scoring

### Files
- `app/schemas/section_draft_output.py`
- `app/tools/tool_wrappers/section_synthesizer.py`

---

## 📦 Draft Chunking

### What It Is
Chunking splits a long GPT-generated draft into a list of paragraphs or sections. These are stored as `draft_chunks` alongside the full text.

### Why We're Doing It
- Enable downstream tools to reuse/edit individual chunks
- Improve trace granularity in `ReasoningTrace`
- Future-proof for token-sensitive tools and UI rendering

### How We Implemented It
- Used `re.split(r'\n\n+', raw_draft)` to split on double newlines
- Stored `draft_chunks` in the validated output schema
- Plan to save chunks in DB via `ReasoningTrace`

### How to Reuse
- Use the `draft_chunks` field in output of any text-generation tool
- For deeper customization, plug in token-aware chunker using Tiktoken

### Future Enhancements
- Add `tokenize_and_chunk()` utility
- Context-aware chunking (e.g., headings, bullet points)
- Diff-based edit tracking per chunk

### Files
- `app/tools/tool_wrappers/section_synthesizer.py`
- `app/schemas/section_draft_output.py`
