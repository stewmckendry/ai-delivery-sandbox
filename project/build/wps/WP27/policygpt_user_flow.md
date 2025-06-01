## GovDoc Copilot: PM Edition – End-to-End User Journey

This guide describes how users interact with the GovDoc Copilot assistant to go from a blank slate to a fully drafted and refined policy or investment artifact. It outlines each step of the journey, the conversations the user might have with the GPT assistant, the tools/chains being invoked, and what’s happening in the background.

---

### 🛫 1. Chat Begins: Context and Gate Setup
**User says:** “I need help drafting materials for a Cabinet submission.”

**GPT replies:** “Which policy gate are you preparing for? For example: Gate 1, 2, or 3?”

**Tool called:** `getArtifactRequirements`
- **Purpose:** Fetches the list of artifacts, sections, and metadata for the selected gate from `gate_reference_v2.yaml`.
- **Inputs:** `{ gate_id }`
- **Background:** GPT uses this map to serve as a navigator for the artifact generation and review.

---

### 🗂 2. Upload Project-Specific Inputs
**User says:** “Here’s our program backgrounder and stakeholder notes.”

**GPT replies:** “Uploading and indexing these as references.”

**Tool(s) called:**
- `ingestInput` (for structured fields)
- `uploadInputPDF`, `uploadInputDocx`, `uploadInputText`

**Background:**
- Content is parsed, chunked, and saved to Redis or vector DB.
- Metadata is stored for later recall.

---

### 📚 3. Align to Government Reference Documents

Official strategy documents, policies, mandate letters, guidelines, and landmark reports help ensure alignment with government priorities and language.

#### A. Browse Available References
**User says:** “What reference documents do we already have?”
- **GPT calls:** `listReferenceDocuments`
- **Purpose:** Fetches unique document titles, sources, and dates currently indexed.
- **Background:** Prevents duplication and encourages reuse of relevant sources.

#### B. Upload New Reference Documents
**User says:** “Here’s the 2025 mandate letter and AI strategy.”
- **GPT calls:** `uploadReferenceDocument`
- **Inputs:** Full text (`file_contents`) or URL (`file_url`), plus metadata (title, source, date).
- **Background:** Document is cleaned, chunked, embedded, and indexed in the PolicyGPT vector database.

#### C. Align with Reference Documents 
**User says:** “What does the government say about AI?” or “How does this align with the Digital Standards?” or "How can I align my proposal with the 2025 mandate letter?"
- **GPT calls:** `alignWithReferenceDocuments`
- **Purpose:** Retrieves relevant excerpts and metadata from indexed documents and generates a summary.
- **Background:** Answers, excerpts, and citations are saved as context for drafting.

---

### 🌍 4. Conduct Additional Research (with GovDoc Copilot: PM Edition)

The assistant helps users explore new issues, analyze context, and conduct open-ended research in the chat interface.

#### A. Discussion and Research
**User says:** “What’s already been done on this issue?” or “Can you find more examples?”
- **GPT searches and synthesizes** using web access and reasoning skills.
- **When useful insights are found:**
  - **GPT says:** “Want me to save this for drafting later?”
  - **GPT calls:** `record_research`
  - **Inputs:** Notes from research or discussion, optionally with metadata.
  - **Background:** Saved with structured tags and citations in PromptLog as `global_context | record_research`.

---

### ✍️ 5. Draft Each Section
**User says:** “Let’s start drafting the Problem Statement.”

**GPT calls:** `generate_section_chain`
- **Steps:** Retrieves memory, inputs, corpus matches, and prompts the LLM.
- **Saves to:** `ArtifactSection` (DB) and `Redis` (live draft)

---

### 🧠 6. Review and Revise Each Section
**User says:** “That could be clearer. Add stakeholder evidence.”

**GPT calls:** `revise_section_chain`
- **Tools used:**
  - `feedback_structurer` – breaks down feedback and assigns sections.
  - `section_rewriter` – rewrites based on revision type.
  - `diff_summarizer` – stores summary in Redis.
  - `save_artifact_and_trace`

**Stored in:**
- `ArtifactSection` (DB)
- Redis (as in-memory “review” version)

**To retrieve:** `fetch_review_section`, `list_review_sections`

---

### 📃 7. Finalize the Document
**User says:** “Looks good. Let’s finalize.”

**GPT calls:** `assemble_artifact_chain`
- Loads section metadata from DB + Redis
- Calls `formatSection`, `mergeSections`, `finalizeDocument`
- Saves to Google Drive via `storeToDrive`

---

### 🔁 8. Return With Feedback
**User says:** “Here’s reviewer feedback from our director.”

**GPT replies:** “Parsing and applying feedback.”

**Tool:** `revise_section_chain` again
- Feedback is restructured, mapped, rewritten, and diffed
- Trace is logged

---

### 🧭 Alternative Paths
- Skip research phase
- Use only uploaded inputs
- Manual edits via `manualEditSync`

---

This design supports async work, stakeholder feedback, traceable changes, and alignment to reference material.
