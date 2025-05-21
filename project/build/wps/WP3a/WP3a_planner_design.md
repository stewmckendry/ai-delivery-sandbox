# WP3a Planner Design Document

## 🎯 Objectives
Design and implement the PolicyGPT Planner + Memory Layer to:
- Interpret user intent and trigger appropriate toolchain
- Persist tool calls and outputs to enable provenance and replay
- Maintain session context and allow full session recovery
- Output structured reasoning traces to support audit and debugging

## 📜 Outcomes & Acceptance Criteria (from WP3a_definition.md)
| Outcome | Criteria |
|---------|----------|
| Planner orchestrates task flow | Given an intent, planner selects correct toolchain and tracks task state |
| Logs are persisted | Each planner step is logged with metadata and full I/O, and stored for replay |
| Memory model is aligned | PromptLog and SessionSnapshot conform to memory model and allow rehydration |
| Reasoning trace | Planner outputs YAML trace of decision logic and toolchain path |
| CLI executable | Can run planner against example session using CLI, without UI |

## 🧩 Architecture Summary
The planner acts as an orchestrator:
- Interprets intent or trigger (e.g. generate section)
- Looks up valid tools and chains from `tool_catalog`
- Runs tools and logs outputs to `PromptLog`
- Maintains and saves session state to `SessionSnapshot`
- Can run in live (active LLM calls) or replay mode

## 📦 Deliverables & Files
| ID | Task | Output |
|----|------|--------|
| T1 | Design strategy and fallback logic | WP3a_planner_design.md |
| T2 | Planner engine | app/engines/planner_orchestrator.py |
| T3 | Memory + trace writer | app/engines/memory_sync.py |
| T4 | PromptLog model | app/db/models/PromptLog.py |
| T5 | SessionSnapshot model | app/db/models/SessionSnapshot.py |
| T6 | YAML schema + tests | WP3a_memory_schema.md, WP3a_test_cases.md |

## ⚙️ Planner Modes
- **Live Mode**: Execute tools, log real responses
- **Replay Mode**: Load from PromptLog + SessionSnapshot, no tool execution

## 🔁 CLI First Workflow
- Example CLI runs planner with intent + inputs
- Logs outputs + trace
- Supports confidence testing before UI integration

## 📐 Schema Strategy
- Align early with `session_memory_model_v2.md`
- Allow extensions (e.g., file links, user tag)
- Store full input/output externally if needed

## 🔁 Trace Format
```yaml
reasoning_trace:
  task_id: draft-section
  planner_decisions:
    - step: analyze-goal
      tool: intent_classifier
      input: "generate outputs section"
      output: "intent: generate_section"
    - step: fetch-schema
      tool: schema_loader
      input: "section_type: outputs"
      output: "loaded schema for outputs"
```

## 🔐 Assumptions
- Planner is triggered explicitly by intent (not passive)
- Full I/O logging is retained for replay + debugging
- Tools will be modular and described in tool catalog

## 🧪 Testing Plan
- CLI trigger with test session
- Memory log assertions
- Trace output validation
- Replay mode step-through

## 📌 Notes
- CLI-first avoids UI dependency and supports headless QA
- Reference data will be Git-hosted where feasible
- Planner chain logic will be modular for reuse

---
Ready to begin T2: implement `planner_orchestrator.py`.
