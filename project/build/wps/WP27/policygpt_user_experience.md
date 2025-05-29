## PolicyGPT User Experience: Gating Artifact Generation

### 1. Proposed User Experience Flow

#### (1) Kick-Off
- User initiates with goal (e.g., "I'm here to prepare for gate 1?")
- GPT queries project metadata or gate reference to suggest artifacts (e.g., Business Case, Project Charter)
- User selects artifact

#### (2) Inputs + Research
- User uploads documentation, notes, or corpuses
- GPT processes and summarizes, seeks confirmation before saving (via injectInputChain)
- GPT offers research support (e.g., corpus, web search, GoC alignment)
  - User can choose global search or step-by-step tool use
  - GPT saves confirmed results

#### (3) Drafting
- User chooses section-by-section drafting or auto-pilot mode
  - Section-by-section: generate_section_chain with memory/context inputs and user feedback
  - Auto-pilot: generate_artifact_chain iterates over all sections with persistent context
- After all sections, GPT assembles the artifact using assemble_artifact_chain

#### (4) Stakeholder Feedback / Revisions
- User uploads feedback content
- GPT summarizes and confirms with user
- revise_section_chain used to apply changes
- Finalization step offers Drive link with completed artifact

---

### 2. Assessment & Thoughts

**Strengths:**
- Clear checkpoints for human-in-the-loop control
- Flexible UX for beginners and power users
- Modular design allows future enhancement

**Risks:**
- Token limits may constrain artifact-wide context
- Summarization quality is critical to maintain content fidelity

**Feasibility:**
- Toolchains and tools can support this flow with moderate refactors
- Minimal new tool creation needed; mostly chain orchestration and prompt logging

---

### 3. Recommendations
- ✅ Proceed with this UX flow
- 📌 Separate summarization step to feed generate_section/chain
- 🔁 Log all global context separately in memory with explicit tags for retrieval
- 🧠 Design feedback schema for logging and reusing user edits/revisions

---

### 4. Implementation Plan

#### Iteration 3
- Implement summarization utility for context inputs
- Develop global_context toolchain to extract, summarize, and log inputs and research
- Refactor generate_section_chain to rely on global_context not internal calls
- Validate end-to-end artifact creation with section-by-section mode

#### Iteration 4
- Implement revise_section_chain
- Enhance feedback parsing from user-provided comments and docs
- Extend generate_artifact_chain with feedback revision support
- Add Drive integration for final deliverables

---

### 5. Updated Task List (WP27)
- Added to `iteration_3_task_list.md`
- Tasks: summarization utility, global_context chain, UX hook scripting, toolchain refactors

---