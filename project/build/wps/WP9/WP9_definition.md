## WP ID: WP9
## WP Name: Input Ingestion + Summarizer

### 🌟 Outcome
By the end of this WP, as a **policy drafter**, I will be able to upload, ingest, and summarize a variety of project inputs (e.g., briefings, transcripts, strategy docs). This enables faster onboarding to context, reduces manual summarization work, and ensures relevant signals are extracted for gate artifact drafting.

### 🧽 Scope
**In Scope:**
- Uploading and parsing unstructured files (text, PDF, etc.)
- Summarization of input content with section labeling
- Retry logic for failed or partial extractions
- Planner-compatible tool interfaces

**Out of Scope:**
- Guided user input prompts (future WP16)
- Evidence lookup or citation tagging (WP8)
- Structured plan generation (WP3a)

### 📦 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/tools/structured_input_ingestor.py` | Parses and labels user inputs |
| `app/tools/retry_ingestion.py` | Adds retry/backoff logic on ingestion failure |
| `app/tools/text_extractor.py` | Extracts content from file uploads |

### 📄 Supporting Documentation (to generate)
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WP9/WP9_input_summary_flow.md` | How inputs are processed, labeled, and summarized |

### ✅ Acceptance Criteria
- [ ] Users can upload input files (chat-based or UI drop-in)
- [ ] Uploaded inputs are labeled, summarized, and available to planner
- [ ] Retry logic handles 404s or parsing errors
- [ ] Outputs are planner-compatible YAML for use in downstream toolchains

### 🛠 Tasks
| Task ID | Description |
|---------|-------------|
| T1 | Build `text_extractor.py` for parsing files |
| T2 | Build `structured_input_ingestor.py` for labeling inputs |
| T3 | Add retry logic to ingestion flow |
| T4 | Generate flow diagram of input summary path |
| T5 | Register tools for planner access (via WP3a) |

### 📚 Reference Documentation
| File Path | Usage |
|-----------|--------|
| `gate_reference.yaml` | Determines what inputs are needed for gate artifacts |
| `tool_catalog_v2.md` | Describes ingestion-related tools |
| `session_memory_model_v2.md` | Mid-term memory capture of user input summaries |

### 📝 Notes to Development Team
- Ingested inputs will be stored in mid-term memory (e.g., `planner_task_trace.yaml`, `SessionSnapshot`)
- Planner (WP3a) can request summaries or raw inputs as part of section drafting
- Failure handling should log to `ErrorLog` (via WP3c)

### 🧠 Clarifications
- 🔠 **User Input Types:** Includes freeform text, file uploads (PDF, .docx), and structured forms (future)
- 🔍 **Hybrid UX:** Users can upload freely OR be prompted by GPT for needed inputs per gate artifact (future WP16)
- ✅ **Planner Trigger:** Planner will detect missing inputs and request them using toolchain flow (WP3a)
- 👁️ **Traceability:** Ingested content will be cited via WP8 when used to justify claims or policy text
