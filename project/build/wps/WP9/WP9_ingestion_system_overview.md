## Ingestion System Overview (WP9)

### 🔄 Purpose
The ingestion system enables Pods and planners to input structured content from various sources (text, files, URLs) into the memory system, with full traceability and logging.

### 🧩 Components

#### 1. `cli_ingest_runner.py`
- CLI wrapper to trigger any ingestion tool
- Handles file reading, input structuring, and tool dispatch

#### 2. `structure_input()` (in `structured_input_ingestor.py`)
- Generates standardized input payloads with UUIDs, timestamps, summaries, and metadata

#### 3. Ingestion Tools
- `uploadTextInput.py`: Handles freeform text
- `uploadFileInput.py`: Handles PDFs/DOCX via `text_extractor`
- `uploadLinkInput.py`: Uses URL extractors (e.g., `newspaper3k`)

#### 4. Logging
- `log_tool_usage(...)`: Writes YAML file to `logs/ingest_traces/`
- Adds DB record via `PromptLog` ORM

#### 5. Retry Logic
- `retry_ingestion.py`: Exponential backoff for transient ingestion errors

### ✅ Example CLI Usage
```bash
python3 -m app.tools.tool_wrappers.cli_ingest_runner logs/input_traces/samples/example.txt --type uploadTextInput
```

### 📦 Outputs
- YAML: `logs/ingest_traces/<uuid>.yaml`
- DB: PromptLog table with tool name, summary, timestamp, etc.

### 📌 Notes
- Inputs are auto-tagged (`input`, `upload`) for searchability
- YAML format standardizes data across sources

Use this system for adding any new ingestion modality. Simply create a wrapper tool and register it with the CLI runner.

— ProductPod