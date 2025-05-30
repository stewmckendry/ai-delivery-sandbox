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