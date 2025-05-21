## WP1a Design Document – Scaffolding & Assembly

### 🎯 Purpose
This document defines the design for WP1a: build tools to scaffold, expand, and assemble high-quality gate-based draft documents based on `gate_reference.yaml`. It aligns with the broader PolicyGPT system architecture and interfaces.

---

## ✅ Outcomes & Acceptance Criteria

**From WP1a_definition.md**:
- [x] Tool to scaffold section-by-section layout from gate spec
- [x] Tool to expand section layout using memory context
- [x] Tool to assemble expanded sections into final doc
- [x] Output matches formatting and quality expectations
- [x] Includes unit and integration tests
- [x] Modular and usable by other Pods

### Traceability
Each component maps to acceptance criteria and ties into the system’s modular build flow.

---

## 🏗️ Components

### 1. `gate_section_scaffolder.py`
- Input: Gate ID
- Reads: `gate_reference.yaml`
- Output: JSON scaffold with layout placeholders
- Metadata: `section_id`, `title`, `next_pod_hint`

### 2. `gate_section_expander.py`
- Input: JSON scaffold + memory context (session ID)
- Uses: Memory API per `session_memory_model_v2.md`
- Output: Expanded draft sections, GPT-generated

### 3. `final_document_assembler.py`
- Input: List of expanded sections
- Output:
  - `docs/working/<doc_id>.md`
  - `docs/working/<doc_id>_gateblock.json`
- Metadata includes traceability and timestamps

---

## 🧰 Interfaces & Standards
- Input/output matches `api_contracts_v2.md`
- Errors follow `error_handling_matrix_v2.md`
- Modular functions enable CLI or Pod-triggered use

---

## 🔁 Integration & Routing
- Scaffolder includes optional `next_pod_hint` to support downstream flow triggers
- All tools log key metadata to enable orchestration by session agent or router

---

## 🧪 Testing Plan
- See `WP1a_tests.md`
- Unit tests: config parsing, memory expansion, assembly order
- Integration tests: end-to-end gate-to-doc generation

---

## 📦 Outputs
| Tool | Output Path |
|------|-------------|
| Scaffolder | `app/tools/gate_section_scaffolder.py` |
| Expander   | `app/tools/gate_section_expander.py` |
| Assembler  | `app/templates/final_document_assembler.py` |
| Markdown Output | `docs/working/<doc_id>.md` |
| JSON Output     | `docs/working/<doc_id>_gateblock.json` |

---

## 📚 References
- `gate_reference_v2.yaml`
- `session_memory_model_v2.md`
- `api_contracts_v2.md`
- `gating_doc_quality_v2.md`
- `system_architecture_v2.md`