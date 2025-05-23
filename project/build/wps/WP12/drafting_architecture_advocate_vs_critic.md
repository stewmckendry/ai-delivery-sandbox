# Evaluating Drafting Architecture: Advocate vs. Critic

## Clarification of Current Design

In the current PolicyGPT architecture:
- Drafting is performed in the backend via the `compose_and_cite` tool.
- This tool is executed as part of a **Planner toolchain**, orchestrated autonomously.
- It uses OpenAI’s **Chat Completion API** to generate content.
- The **Custom GPT UI (frontend)** does **not** directly generate content using its own chat-based LLM capabilities.

### Why? 
To keep drafting consistent, evidence-based, and validated — independent of volatile, session-limited frontend context.

---

## **Advocate Perspective: Why This Design Makes Sense**

### Design Rationale
1. **Traceable and Structured Generation**
   - Drafts must meet gate-specific criteria and be auditable.
   - A toolchain like `compose_and_cite` can:
     - Inject validated evidence
     - Enforce schema rules
     - Validate drafts pre-save

2. **Centralized Control + Memory Reuse**
   - Planner and memory YAMLs (`reasoning_trace.yaml`, `planner_task_trace.yaml`) enable rehydration, reuse, and repeatability.
   - These are **not accessible in chat LLM memory**.

3. **Token Budget Management**
   - Backend tools chunk long content, stitch results, and avoid UI-based token bloat.

4. **User Experience Focus**
   - GPT UI serves as a review, edit, and feedback surface.
   - Drafts feel pre-structured, accurate, and are not vulnerable to hallucination.

### What I’d Do the Same (or Better)
- Keep planner-drafted flow for auditability.
- Enhance GPT UI to **narrate planner reasoning** and **let user choose Auto vs Assisted drafting.**
- Create a new endpoint:
  ```
  /tasks/view_draft_plan
  ```
  Returns the draft plan, inputs, and expected outputs for preview.

### Deliverables
| Path | Description |
|------|-------------|
| `/tasks/view_draft_plan` | Returns section plan, trace inputs, and tools before execution |
| `/ui/gpt_draft_choice_prompt.md` | GPT script that prompts user to choose Assisted vs Auto path |

---

## **Critic Perspective: Why This Might Be Limiting**

### Design Gaps
1. **Underuse of ChatGPT Superpowers**
   - GPT is strongest in composing content from complex inputs.
   - Not leveraging frontend GPT breaks natural flow of thought.

2. **Loss of Conversational Iteration**
   - Users may want to co-create — not just review generated text.
   - Current design forces a batch process.

3. **Technical Overhead + Latency**
   - Planner toolchain execution adds latency.
   - Invoking multiple backend tools increases cost and potential failure points.

### What I’d Do Differently (While Preserving Goals)
**Hybrid Drafting Flow**:
- Let GPT draft a section **live in the chat UI** using LLM tools.
- **Use planner only to validate, reformat, and commit.**

#### Technical Flow
1. User uploads inputs via `uploadTextInput` or file
2. GPT loads memory YAML + PromptLog summary
3. GPT calls OpenAI API directly with project profile and embedded research
4. Draft appears live in chat
5. GPT prompts user: “Should I validate + commit this?”
6. GPT then calls planner:
   - `validateSection`
   - `commitSection`
   - `logReasoningTrace`

### Required Changes
| Path | Description |
|------|-------------|
| `/tools/gpt_direct_draft.py` | Wrapper for live GPT chat drafting using token-balanced plan |
| `/ui/chat_draft_scripting.md` | Prompt template for frontend GPT drafting with structure and citations |

---

## Evaluation: Goals vs UX vs Feasibility

| Criterion | Backend Toolchain | ChatGPT Drafting |
|----------|-------------------|------------------|
| **PolicyGPT Goal: Structured, Validated Docs** | Strong (toolchain enforces rigor) | Needs planner validation stage |
| **User Experience** | Clear UX control, but disconnected | More fluid, collaborative |
| **Reuse + Auditability** | Strong via memory YAMLs | Needs work to persist trace |
| **Token Management** | Centralized, chunk-aware | Risk of session overflow |
| **Frontend Simplicity** | UI is simpler, outputs pre-baked | UI needs tooling and gating UX |

---

## Recommended Next Step
Consider a **dual-mode approach**:
- Default: Planner-managed generation
- Opt-in: GPT-led chat drafting with post-validation and trace logging

---

## Summary
The backend-first approach ensures rigor and traceability. But offering GPT-driven chat drafting could unlock more collaborative experiences — provided planner validation is preserved. A hybrid model with clear gating and trace capture could offer the best of both worlds.