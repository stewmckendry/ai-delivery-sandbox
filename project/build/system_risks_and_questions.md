## System Risks and Open Questions Log

### Draft Generation Ambiguity (Logged: 2025-05-22)

**Issue:**
It is unclear where and how the drafting of gate artifacts actually happens:
- WP16 is building a UI for user inputs, leveraging WP9’s upload tools.
- The toolchain supports chaining tools like `compose_and_cite`, but this tool has not yet been built.
- The DB schema includes `ArtifactSection`, but it is not yet linked to a clear generation flow.

**Key Questions:**
1. Is the artifact draft created by GPT within the custom ChatGPT UI (real-time generation)?
2. Or does the draft generation happen in the backend, via tool calls (like `compose_and_cite`) using OpenAI APIs?
3. Or is it a hybrid — where backend tools prime or scaffold content and the GPT in the UI drafts iteratively with the user?

**Implications:**
- **User Experience:** Where is the user iteratively drafting with PolicyGPT?
- **Quality Expectations:** Can either path support deep research-level document generation?
- **Tech Constraints:** API/token limits, GPT summarization bias, session context size management, and modular composition.

**Action Needed:**
Escalate to WP12 (System Design Pod) for investigation and resolution.

**Suggested Deliverables:**
- Updated data flow and component interaction model
- Clarification of end-to-end user experience from input to artifact output
- Design alignment between UI flow, toolchain, and memory/session management

**Status:** Open
**Assigned to:** WP12
**Origin:** Observed by Lead Pod during WP16 and WP9 coordination

---

Future system-level risks and design issues should be appended here as they emerge.