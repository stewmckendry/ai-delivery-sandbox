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

## 💡 Recommendations

1. **Extract Orchestration Logic to Code**
   - Use `planner_orchestrator.py` to encode orchestration as first-class pipeline, not GPT reasoning.

2. **Define Explicit Output Schemas**
   - Formalize contracts for: `composeDraft`, `validateSection`, `commitSection`
   - Use JSONSchema or Pydantic to validate outputs before DB insert

3. **Batch + Retry + Stream Draft Generation**
   - Use generator functions or async workers to chunk and retry parts
   - Especially useful for large artifacts or limited tokens

4. **Log Contracts in ReasoningTrace**
   - Append versioned tool specs to each trace
   - Enables reproducibility and testable planning

5. **Clarify GPT Role in UI vs Backend**
   - GPT should propose, not execute toolchains
   - UI should call composite services (Planner Phase Services)

---

## 🛠️ Action Plan

| Deliverable | Function | Notes |
|------------|----------|-------|
| `/orchestrator/section_plan_runner.py` | Code wrapper for compose + validate + commit | Replaces GPT-driven sequences |
| `/schemas/section_draft.schema.json` | JSON schema for section output | Used by all drafting tools |
| Update `planner_task_trace.yaml` | Include output contract refs | Toolchain doc clarity |
| Patch `ReasoningTrace` writer | Add schema version + contract log | Improves auditability |
| UI-GPT behavior spec | Define GPT role as proposer only | Aligns with orchestrator usage |

---

## 📘 Summary
PolicyGPT is well-aligned with many MCP design principles, but can benefit from stronger code orchestration boundaries, output validation, and LLM-role clarity. These changes improve scaling, testability, and governance for high-value document pipelines.