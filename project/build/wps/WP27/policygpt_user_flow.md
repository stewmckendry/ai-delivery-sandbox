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

### 📚 3. Reference Key Policy Documents (Upload or Browse)

#### A. Upload Reference Documents
**User says:** “Here’s the 2025 mandate letter and strategy doc.”

**GPT calls:** `uploadReferenceDocument`
- **Inputs:** Accepts full text (`file_contents`) or a link (`file_url`), with metadata (title, source, date).
- **Background:**
  - Texts are chunked, embedded, and stored in the "PolicyGPT" vector DB.
  - Metadata is indexed for citation and reuse.

#### B. List What’s Already Uploaded
**User says:** “What reference documents do we already have?”

**GPT calls:** `listReferenceDocuments`
- **Purpose:** Retrieves a list of indexed documents in the corpus for review or reuse.
- **Background:** Prevents duplication and surfaces prior uploads to build on.

---

### 🌍 4. Build Global Context (Optional Research)

**User says:** “What’s already been done on this issue?” or “Here’s something I found – can you record it?”

#### A. DIY Research with GPT (Discovery Mode)

**User and GPT discuss and explore manually.**

- **GPT Says:** "Let me help you summarize that. Want me to save this as context for the draft?"
- **GPT calls:** `record_research` with:
  - `notes`: User-GPT discussion or pasted research
  - `session_id`, `project_id`

**Background:**
- Notes are cleaned up using GPT.
- Saved with structured metadata and citations.
- Indexed in PromptLog as `"global_context | record_research"` for later reuse.

#### B. Automated Research (Backend Tools)

**GPT Says:** “I’ll search the web and internal sources.”

- **GPT calls:** `global_context_chain` → runs:
  - `webSearch`
  - `queryCorpus`

**Background:**
- Controlled prompt templates used.
- Logs saved to PromptLog with `"global_context | {tool_id}"`.
- Results are summarized and cited.
- Indexed for draft alignment.

In both flows, content is fetched in `generate_section_chain` to inform GPT when drafting.

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
