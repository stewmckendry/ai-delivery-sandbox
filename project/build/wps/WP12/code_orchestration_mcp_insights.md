# Code Orchestration Insights from MCP Model for PolicyGPT

## 🔍 Overview
This report analyzes the article "LLM function calls don't scale; code orchestration is simpler, more effective" (https://jngiam.bearblog.dev/mcp-large-data/) and assesses its applicability to the PolicyGPT system, especially in light of the dense artifact generation design and ongoing toolchain development.

---

## 🧠 Key Insights from MCP Article

### 1. **Function Calls vs Code Orchestration**
- **LLM function calls** are limited by token context, fragile formats (e.g., large JSONs), and hallucination risks.
- **Code orchestration** separates logic and state into executable code outside the LLM, improving efficiency, transparency, and reusability.

### 2. **Output Contracts and Schemas**
- Stable, versioned schemas ensure predictable inter-tool outputs.
- Avoids brittle prompt engineering for parsing JSON in LLM responses.

### 3. **Streaming + Batching**
- Chunk large tasks into small, retryable, and cacheable code steps.
- Enables memory-efficient processing and pipeline resiliency.

---

## 🧩 Relevance to PolicyGPT

PolicyGPT already exhibits several design patterns aligned with the article:
- Use of backend `compose_and_cite`, `validateSection`, and `logReasoningTrace` tools for chunked, multi-step LLM interaction
- YAML-based schemas (`planner_task_trace.yaml`, `project_profile.yaml`) for planner coordination
- Explicit schema-based logs (`ArtifactSection`, `ReasoningTrace`) in DB

**However**, PolicyGPT currently:
- Relies on LLM to handle logic that could be better expressed in code (e.g., template selection, summarization decisions)
- Lacks robust validation/contract checking on LLM outputs pre-DB write
- Does not clearly separate orchestration from UI-level GPT behavior

---

## 🔍 Alignment vs Gaps

| Area | Aligned | Gaps / Risks |
|------|---------|--------------|
| Toolchain execution | ✅ Planner and tool-based execution (WP17b) | ❌ Coupled planner logic + LLM prompts |
| Data schemas | ✅ YAML + SQL models | ❌ No schema enforcement at runtime |
| Chunking | ✅ Uses `get_token_usage`, breaks into sections | ❌ Not streaming or cacheable/retryable chunks |
| Output contracts | ✅ Defined markdown + trace logs | ❌ No schema validation between tools or tool versions |
| UI vs Backend Roles | ❌ GPT sometimes orchestrates + composes | ❌ Leads to drift, token overflow, fragile flows |

---

## 💡 Recommendations (with Detail)

### 1. Extract Orchestration Logic to Code
- Move tool sequencing from GPT to Python (`section_plan_runner.py`)
- Keeps planner logic consistent, testable, and error-resistant

### 2. Define Explicit Output Schemas
- Create schemas for `compose_and_cite`, `validate_section`, etc.
- Use tools like JSONSchema or Pydantic to check outputs before saving

### 3. Batch + Retry + Stream Draft Generation
- Generate one section (or chunk) at a time with retry logic
- Reduces token usage, isolates errors, enables partial caching

### 4. Log Contracts in ReasoningTrace
- Each tool run should log version of the tool and schema used
- Enables traceability and audit

### 5. Clarify GPT Role in UI vs Backend
- GPT proposes the next step, but code (or composite endpoint) executes it
- Prevents hallucination and keeps GPT focused on assisting users

---

## ✋ User Interaction Flow (E2E)

| Phase | User Action | GPT Action | Tool Calls |
|-------|-------------|------------|------------|
| Start | Uploads inputs | Summarizes inputs | `describe_file`, `index_memory` |
| Setup | Confirms draft target | Asks to start draft plan | `prepare_drafting_context` |
| Plan | - | Narrates plan | `propose_draft_plan` |
| Draft | Waits or watches | Proposes to run draft | `execute_draft_phase` |
| Review | Provides feedback | Revises or re-runs step | `execute_draft_phase` (revised) |
| Approve | Says “looks good” | Triggers validate + save | `validate_and_commit` |

---

## 🛠️ Action Plan

| Deliverable | Function | Notes |
|------------|----------|-------|
| `/orchestrator/section_plan_runner.py` | Encodes draft plan logic | Replaces GPT prompt chains |
| `/schemas/section_draft.schema.json` | Draft output schema | Used by `compose_and_cite` |
| `planner_task_trace.yaml` patch | Logs contracts used | Adds traceability |
| ReasoningTrace patch | Includes schema + tool version | Improves audit trails |
| UI behavior spec | Clarifies GPT is helper not executor | Supports Planner Phase Services |

---

## 📘 Summary
PolicyGPT is well-aligned with many MCP design principles, but needs to strengthen its orchestration model by extracting logic into code, enforcing output schemas, and cleanly separating GPT’s UI role from tool execution. This improves resilience, scalability, and audit readiness.

---

## Appendix: Recommendation Details

### 1. Extract Orchestration Logic to Code

**What it means:**  
Right now, GPT sometimes decides the tool order (e.g., “let’s search, then compose, then validate”). This logic lives in prompts or system messages. Instead, we should move this decision-making into a Python file — like a recipe.

**Example:**  
A file like `section_plan_runner.py` would say:  
“If the user wants a Risk Management section, first call `searchKnowledgeBase`, then `compose_and_cite`, then `validate_section`, and finally `commit_section`.”

**Why it matters:**
- Easier to test  
- Consistent results  
- Less chance for GPT to forget steps or go off-script

**Change needed:**
- Add a module `/orchestrator/section_plan_runner.py`
- Update WP17b scope to delegate planning to this code file instead of having GPT figure it out in chat

---

### 2. Define Explicit Output Schemas

**What it means:**  
Right now, tools return markdown or JSON but there’s no strong enforcement of format. We should define a standard schema — like a blueprint — for what every tool output must include.

**Example:**  
A JSON schema for a drafted section might look like:
```json
{
  "section_type": "string",
  "content": "markdown",
  "citations": ["url"],
  "validation_status": "valid" or "needs_review"
}
```

**Why it matters:**
- Catch errors early  
- Enforce consistency across tools  
- Prevent invalid data going into the database or Drive

**Change needed:**
- Create `/schemas/section_draft.schema.json`  
- Patch `compose_and_cite` and `validate_section` to output this schema  
- Add schema check step before `commit_section` is called

---

### 3. Batch + Retry + Stream Draft Generation

**What it means:**  
Break up long drafts into smaller parts (sections, subsections), generate each separately, and retry any that fail.

**Example:**  
If the Program Plan has 8 sections, the planner should:
- Plan and run each section separately  
- Retry a section if it hits an OpenAI error  
- Cache completed sections to avoid rework

**Why it matters:**
- Reduces token use  
- Handles failures more gracefully  
- Enables parallelism and future scaling

**Change needed:**
- Update `planner_task_trace.yaml` to chunk work  
- Add retry logic to `section_plan_runner.py`  
- Extend WP17b to handle draft status per section or chunk

---

### 4. Log Contracts in ReasoningTrace

**What it means:**  
Every time a tool runs, we should log which version of schema or contract it used, so we can trace how a section was created.

**Example:**  
A `ReasoningTrace` might say:  
“Used `compose_and_cite` v3.2 with output schema v1.0. Draft passed validation and was committed.”

**Why it matters:**
- Traceability for audits  
- Easier debugging  
- Confidence in draft quality

**Change needed:**
- Patch `logReasoningTrace` to include contract version metadata  
- Update WP17b to include contract logging as part of draft pipeline

---

### 5. Clarify GPT Role in UI vs Backend

**What it means:**  
GPT (the chat assistant) should help the user understand what’s happening and gather inputs — not be the one deciding or executing tool sequences.

**Example:**  
Instead of GPT saying:  
“I’m now generating your Risk Management section...”  
GPT should say:  
“I’ve prepared your inputs. Should I ask the planner to start drafting the Risk Management section?”

**Why it matters:**
- Keeps GPT sessions lighter and safer  
- Makes the backend responsible for orchestration  
- Makes system easier to test and maintain

**Change needed:**
- Update GPT system prompt and handoff logic  
- Update WP16 and WP17b to use Planner Phase Services or composite endpoints, not individual tool calls from GPT
