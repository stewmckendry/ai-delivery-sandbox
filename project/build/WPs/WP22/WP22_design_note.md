# 🧠 WP22 Design Note – GoC Alignment Search Tool

## 🎯 Goal
Develop a tool that helps identify alignment between drafted artifact sections and known Government of Canada (GoC) priorities and policies.

---

## 🔍 What It Does
- Accepts a section draft or summary
- Scans relevant GoC content (mandate letters, policies, strategies)
- Returns top semantic matches with snippets and sources
- Supports planner + GPT integration via toolchain

---

## 🛠️ Implementation Strategy

### 🅰 Option A: Query Embedded Corpus
- Use `loadCorpus.py` to pre-load PDFs and documents
- Build `queryCorpus.py` using Chroma or LangChain retrieval
- Pros: Fast, works offline
- Cons: Requires manual updates for new sources

### 🅱 Option B: Targeted Web Search
- Scrape GoC sites (e.g., Canada.ca, department sites)
- Summarize and parse for matches via LLM prompts
- Pros: Always up to date
- Cons: May miss context or require scraping

### ✅ Hybrid Plan
- Try embedded corpus query first
- Fall back to targeted search if corpus hit rate is low
- Format output for use in downstream tools

---

## 🔁 Toolchain Integration
- Register as `goc_alignment_search`
- Add as optional step to `generate_section_chain`
- Output format:
```json
{
  "alignment_summary": "...",
  "citations": ["source_url_or_title"]
}
```

---

## 📂 Suggested Files
- `app/tools/tool_wrappers/goc_alignment_search.py`
- `app/tools/tool_wrappers/queryCorpus.py`
- `project/prompts/goc_alignment_prompts.yaml`

---

## 📘 Reference
- `loadCorpus.py`
- `generate_section_chain.py`
- `section_synthesizer.py`
- `memory_sync.py`, `PromptLog.py`, `ReasoningTrace.py`

---

## 🧠 Lessons Learned
- Trace output, prompt used, and citations
- Validate schema and log usage
- Compose toolchains that are flexible and robust
