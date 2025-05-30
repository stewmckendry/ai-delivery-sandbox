## 1. loadCorpus: Enhancing Usability and Scalability

**Current State:**  
- The tool requires `file_contents` as input, meaning documents must be pre-parsed and provided as raw text.
- This works for short files or pasted text in ChatGPT, but not for lengthy PDFs or web documents.

**Pain Points:**  
- Large PDFs can exceed token/context limits.
- Users must manually convert files or rely on frontend logic.
- GPTs cannot natively fetch URLs, so external content must be processed separately.

**Recommendation:**  
- Extend `loadCorpus` to accept a `file_url` parameter.
    - If `file_url` is provided, the backend fetches and processes the content.
    - Use libraries to:
        - Detect file type (PDF, HTML, etc.).
        - Extract and clean text (e.g., with `pdfplumber`, `BeautifulSoup`).
        - Optionally chunk and embed content for search.

**Benefits:**  
- Makes `loadCorpus` more GPT-friendly.
- Enables workflows like: “Here’s the 2025 Mandate Letter. Load it into PolicyGPT.”
- Supports both file uploads and URL-based sources for alignment and reference.

---

## 2. global_context_chain & External Search: Combining Structure with LLM Flexibility

**Current State:**  
- Backend toolchains (`web_search`, `queryCorpus`, `goc_alignment_search`) are invoked by GPT.
- These handle queries, manage prompting, and return structured results.
- All actions are logged with consistent formats.

**Advantages:**  
- Strong logging and traceability (important for audits and reproducibility).
- Prompt control ensures consistent, high-quality queries to external systems.
- Search results are stored and used in downstream processes.

**Limitations:**  
- Slower iteration—GPT must wait for tool responses.
- Less spontaneity—GPT cannot freely explore or “think out loud.”
- Users may miss the sense of GPT’s exploratory reasoning.

**Recommendation:**  
- Retain structured tools for canonical flows (e.g., mandated alignment checks).
- Add a free-form “discovery” tool:
    - Allow GPT to perform exploratory searches using web-browsing capabilities.
    - Cache or summarize useful results into structured tools as needed.

**Hybrid Approach:**  
- Treat structured tools as “back-office research assistants.”
- Use GPT-native web search for “front office brainstorming” to help users explore unknowns.

---

## Hybrid Discovery Search: Design Summary

### 🔍 Objective
Enable PolicyGPT to flexibly balance structured and free-form information discovery by combining backend tools (for traceability and control) with GPT's native browsing capabilities (for exploratory search).

### ✅ Design Overview

#### 1. Maintain Structured Search Tools for Canonical Tasks
- **Tools:** `web_search`, `goc_alignment_search`, `queryCorpus`
- **Use Cases:** When traceability, versioning, or specific filters are required.
- **Logging:** Outputs are logged in `PromptLog` or memory store for downstream reuse.

#### 2. Add a New Discovery Tool for Free-form Exploration
- **Approach:** GPT initiates web search via native browsing.
- **Integration:** Findings can be cached or converted into structured entries if useful.

---

### (a) Deciding Between GPT-Native and Backend Searches

| Search Type                                      | Method                   | Reason                                   |
|--------------------------------------------------|--------------------------|------------------------------------------|
| What does the 2025 Budget say about transit?     | GPT with browsing        | Exploratory and open-ended               |
| List federal priorities in 2023 Mandate Letters  | Backend with web_search  | Canonical reference, traceable           |
| Check alignment to Digital Policy                | queryCorpus              | Controlled against internal documents    |
| Summarize new bills in Parliament                | GPT browsing             | Dynamic, fast-changing content           |

---

### (b) Changes to Global Context Chain

- Refactor `global_context_chain` to call a `discovery_or_backend_router` step.
- GPT decides the path based on structured signals:
    - `topic=mandate_letter` → `web_search`
    - `topic=emerging_trends` → GPT discovery

---

### (c) New Tool: `discovery_search`

**Inputs:**
```json
{
  "query": "What are Canada's clean tech priorities in 2025?",
  "purpose": "alignment",
  "project_id": "xyz",
  "session_id": "abc"
}
```

**Steps:**
1. GPT uses browsing tools to perform the search.
2. GPT returns:
    - Summary
    - Key URLs
    - Extracts/snippets
3. Tool writes to `PromptLog` with:
    - Query and results
    - GPT-assigned tags (topics, relevance)

**Outputs:**
```json
{
  "summary": "...",
  "key_points": [...],
  "sources": [ {"url": "...", "snippet": "..."} ]
}
```

---

### (d) Task List

- [x] Patch: `loadCorpus.py` to support `file_url`
- [ ] Create Tool: `discovery_search`
- [ ] Patch: `global_context_chain.py` with discovery router
- [ ] Prompt Template: `discovery_search_prompt.yaml`
- [ ] Log: `PromptLog` write for discovery output
- [ ] Doc: Create WP on Hybrid Discovery Strategy

---
## 🧼 loadCorpus via `file_url`: Handling Raw HTML

When ingesting web content, `response.text` retrieves the raw HTML, which is often noisy and inconsistent.

### 🔧 Best Practices for HTML Content Ingestion

- **Use BeautifulSoup** to parse and clean HTML:
    - Strip out `<script>`, `<style>`, `<nav>`, `<footer>`, and similar non-content elements.
    - Prioritize extracting from `<article>`, `<main>`, or `<div class="content">` tags.
- **Apply heuristics** to filter content:
    - Focus on longer paragraphs and higher sentence density.
    - Avoid navigation menus, disclaimers, and boilerplate.
- **Optional LLM preprocessing:**
    - Use an LLM to further clean or summarize extracted text if needed.

**Recommendation:**  
Update `loadCorpus` to:
- Fetch content with `requests.get(url)`.
- Clean HTML using BeautifulSoup.
- Optionally log both raw and cleaned text for traceability.

---

## 🧠 Splitting Discovery vs Structured Research

Your approach to separate exploratory and structured research flows is sound, while unifying how outputs are logged.

### 🧭 Flow Options

| Flow                | Tool(s)                        | Driven by        | Logging         |
|---------------------|-------------------------------|------------------|-----------------|
| Exploratory search  | `record_research` (was `discovery_search`) | GPT + user       | `PromptLog`     |
| Structured backend  | `global_context_chain`, `web_search`, etc. | User or tool     | `PromptLog`     |

- **Exploratory flows:** Enable GPT autonomy for open-ended research.
- **Structured flows:** Use controlled backends for traceable, reusable outputs.
- **Unified logging:** Both approaches persist results in the same format for downstream use.

---

### ✅ Next Steps

- [ ] Patch `loadCorpus` to include BeautifulSoup cleanup (optionally log raw + cleaned text)
- [ ] Rename and implement `record_research` tool
- [ ] Update `PromptLog` format if needed for shared research entries
- [ ] Write README or working paper explaining the dual-path research strategy

---

# ✅ Updated Design for `record_research` Tool

## 🧠 Who Processes the Research?

ChatGPT (frontend GPT) handles the processing — it cleans, summarizes, and structures research before invoking `record_research`.

**Example GPT prompt:**
> “Please confirm or clean up these research notes and I’ll save them to your project research log. Try to include a title, source, date, and URL if known.”

---

## 📥 Input Schema for `record_research`

GPT sends a structured payload, typically an array of entries:

```json
[
    {
        "text": "Cleaned summary or quote",
        "title": "What is Policy Coherence?",
        "source": "OECD Handbook",
        "date": "2021",
        "url": "https://oecd.org/policy-coherence-guide",
        "citation": "\"What is Policy Coherence?\" OECD Handbook, 2021. https://oecd.org/policy-coherence-guide"
    }
    // ...more entries
]
```

- GPT decides what and how many entries to log at once.

---

## 🪵 Backend: `record_research` Tool

- Validate input is a list of entries.
- For each entry:
    - Log to `PromptLog` using `log_tool_usage(...)`.
    - Use `input_summary = "global_context | record_research"`.
    - Add fallback values if GPT omits fields.

---

## 💡 Benefits

- No backend LLM calls — just storage and logging.
- Leverages ChatGPT’s capabilities, reducing backend complexity.
- Ensures structured metadata for citations.
- Keeps logs discoverable by `generate_section_chain`.

---

# 🧠 record_research: Recording and Structuring User-Guided Research

## Overview

The `record_research` tool enables the PolicyGPT front-end to capture exploratory research performed by users or the GPT assistant. It processes this research with LLM assistance and persists it for reuse in downstream section drafting. This approach complements our structured search tools (`web_search`, `queryCorpus`, `goc_alignment_search`), offering users flexibility while maintaining traceability and consistency.

## Dual-Path Research Strategy

| Path                | Who Drives It                | Examples                                 | Persistence           | Tools                                   |
|---------------------|-----------------------------|------------------------------------------|-----------------------|-----------------------------------------|
| Structured Search   | Backend API tools           | Web search, corpus query, alignment check| Yes (via PromptLog)   | `web_search`, `queryCorpus`, `goc_alignment_search` |
| Exploratory Research| User + ChatGPT (Custom GPT) | Manual browsing, human notes, GPT summary| Yes (via record_research) | `record_research`                      |

## Tool Design

- **Tool ID:** `record_research`
- **Purpose:** Record free-form research notes and structure them into metadata-rich entries.

### Inputs

- `notes`: Raw research notes (**required**)
- `session_id`, `project_id`, `user_id`: Context metadata
- `metadatas` (optional): If already structured, skips LLM step

### Processing

If `metadatas` are missing, the tool uses an LLM prompt to:
- Extract individual entries
- Add metadata fields (title, source, date, etc.)
- Retain raw text for traceability

The output follows the `global_context` schema expected by downstream chains.

### Output Format

```json
{
    "answer": "...",
    "documents": ["..."],
    "citations": ["..."],
    "metadatas": [
        {
            "text": "...",
            "title": "...",
            "source": "...",
            "date": "...",
            "url": "...",
            "citation": "..."
        }
    ]
}
```

## Example Use

**Scenario:** User and GPT browse a government website and summarize 3 key policy findings.  
**ChatGPT Action:** Sends all findings as a bullet list to `record_research`.  
**Tool Result:** Cleaned, structured metadata entries are logged and reused later in `generate_section_chain`.

## Best Practices

- Ask GPT to clearly separate research findings using `###` or bullet points.
- Avoid summarizing—prefer source quotes for evidence.
- Encourage capturing URLs or source titles where possible.