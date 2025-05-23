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