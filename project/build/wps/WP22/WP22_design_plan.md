## 🧠 WP22 Design Plan – GoC Alignment Search Tool

### 🎯 Goal
Enable section-level policy alignment by querying GoC corpora and live content, returning structured summaries and citations.

---

### 🛠️ Architecture Overview

#### 🔌 Entry Tool
- `goc_alignment_search.py`: Planner-compatible wrapper
  - Accepts: `{ draft_text, project_context, section_meta }`
  - Calls either `queryCorpus` or `web_search`
  - Returns: `{ "alignment_summary": "...", "citations": [...] }`

#### 📚 Corpus Search
- `queryCorpus.py`
  - Uses embedded Chroma index
  - Relies on `loadCorpus.py` for ingestion

#### 🌐 Web Fallback
- `search_handlers/goc_alignment.py`
  - Performs GoC-scoped search (e.g. `site:canada.ca`)
  - Prompts from `goc_alignment_prompts.yaml`
  - Reuses `web_search_logger.py`, `web_search_formatter.py`

#### 🧠 Toolchain Integration
- `generate_section_chain.py`: Add optional `alignment_support` call
- Output passed to `section_synthesizer` as memory
- Results logged in `PromptLog` and `ReasoningTrace`

---

### 📁 File Plan

| File | Purpose |
|------|---------|
| `goc_alignment_search.py` | Entry point for tool invocation |
| `queryCorpus.py` | Search pre-embedded GoC policy corpus |
| `search_handlers/goc_alignment.py` | Specialized handler for GoC-scoped web search |
| `goc_alignment_prompts.yaml` | Prompts to structure results |
| `WP22_toolchain_integration_note.md` | Integration doc for system maintainers |