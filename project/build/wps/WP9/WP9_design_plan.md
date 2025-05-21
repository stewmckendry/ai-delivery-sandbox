### 🧠 WP9 Design Plan — Input Ingestion System

#### 🎯 Goal
Enable PolicyGPT to ingest, sanitize, structure, and persist diverse user inputs — including files, links, and direct text — into mid-term memory and YAML traces compatible with planner toolchains.

---

### 🗺️ Scope and Inputs
- From: `WP9_definition.md`, `PolicyGPT_Features v2.md`, `session_memory_model_v2.md`
- Inputs: file uploads (.pdf, .docx, .txt), URLs, raw text
- Outputs: YAML trace logs, structured summaries in memory

---

### 🧩 System Design

#### ⚙️ Components
1. **Tool Wrappers**
   - `uploadTextInput`
   - `uploadFileInput`
   - `uploadLinkInput`
   - Each implements `Tool.run_tool(input_dict)`

2. **Text Extraction Engine**
   - Built in `text_extractor.py`
   - Uses `textract`, `beautifulsoup4`, `python-docx`, etc.
   - Normalizes encoding, extracts plain text

3. **Structured Ingestor**
   - Maps extracted content into YAML summaries
   - Adds source metadata: origin, timestamp, author, type

4. **Memory Writer**
   - Uses `memory_sync.py`
   - Writes prompt logs and session snapshots
   - Ensures each input is replayable

5. **Retry Handler**
   - Implements `retry_ingestion.py`
   - Captures parse/validation errors and retries

---

### ✅ Acceptance Criteria (Mapped)
| Requirement | Approach |
|------------|----------|
| Input types handled | Each tool wrapper targets one input class |
| Structured outputs | YAML + mid-term memory writes, validated via schema |
| CLI testability | CLI entry point will allow local dev and test |
| Error retry | Retry handler wraps all tool calls |
| Toolchain-ready | Schema added to `tool_catalog.yaml` and wrappers structured |

---

### 🧪 Testing Plan
- Inputs: `.pdf`, `.docx`, `.txt`, raw text, URL
- Output: compare YAML trace and memory snapshot against schema
- Log: trace YAML in `/logs/ingest_traces/`, JSON in `/logs/session_snapshots/`

---

### 🧠 Trace Logging Format
```yaml
- source: "my_file.pdf"
  type: "uploadFileInput"
  timestamp: "2025-05-19T13:00Z"
  content_summary: |
    "This document outlines..."
  tags: ["input", "upload"]
```

---

### 🧱 Integration Hooks
- Tool Registry: YAML + OpenAPI ready
- Planner: YAML output can be used as prompt or context
- Mid-Term Memory: Writes to `PromptLog` + `SessionSnapshot`

---

### 🔒 Risk Mitigations
- Parser fails → routed through retry with fallback
- Encoding/format noise → `text_extractor.py` handles normalization
- YAML structure drift → schemas validated via tool registry

---

### 🔗 Interfaces Used
- `tool_registry.py`
- `tool_catalog.yaml`
- `memory_sync.py`
- `planner_orchestrator.py` (indirect)

---