## WP ID: WP3a
## WP Name: Planner + Memory Layer

### 🌟 Outcome
By the end of this WP, as an **autonomous planning engine**, I will be able to decompose user goals into toolchain steps and manage memory and session state across tasks. This enables scalable, transparent task execution and allows for deep provenance tracking and rehydration.

### 🧽 Scope
**In Scope:**
- Planner toolchain breakdown
- Execution trace memory and snapshots
- Raw GPT memory logging
- Session recovery design and hooks

**Out of Scope:**
- Tool orchestration (execution and retries, WP3c)
- Reviewer handoff routing (WP6)
- Final document output or validation (WP1b, WP4)

### 📦 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/engines/planner_orchestrator.py` | Converts user goals into toolchain plans and tracks subtask progress. |
| `app/engines/memory_sync.py` | Writes raw LLM inputs/outputs to memory for provenance and planner recall. |
| `app/db/models/PromptLog.py` | Stores GPT tool invocation details for audit and research use. |
| `app/db/models/SessionSnapshot.py` | Persists in-flight planner state for rehydration and resume capability. |

### 📄 Supporting Documentation (to generate)
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WP3a/WP3a_planner_design.md` | Breakdown of planner logic, orchestration examples, and memory references. |
| `project/build/wps/WP3a/WP3a_test_cases.md` | Planner test flows across user journeys (Gate 1, 2, 3, etc.) |
| `project/build/wps/WP3a/WP3a_memory_schema.md` | Snapshot + log schema mapping + YAML trace structure. |

### ✅ Acceptance Criteria
- [ ] Planner can decompose goals into structured plans
- [ ] Each step is logged into `PromptLog`
- [ ] Full planner state is captured into `SessionSnapshot`
- [ ] Memory can be rehydrated across GPT sessions

### 🛠 Tasks
| Task ID | Description |
|---------|-------------|
| T1 | Design planner strategy + fallback logic |
| T2 | Implement `planner_orchestrator.py` with pluggable steps |
| T3 | Implement `memory_sync.py` with trace formatters |
| T4 | Build `PromptLog.py` to store GPT tool metadata |
| T5 | Build `SessionSnapshot.py` to allow planner resume |
| T6 | Write sample YAMLs and test memory rehydration |

### 📚 Reference Documentation
| File Path | Usage |
|-----------|--------|
| `system_architecture_v2.md` | Planner + tool layering diagram |
| `session_memory_model_v2.md` | Snapshot and memory trace specs |
| `tool_catalog_v2.md` | Toolchain definitions planner can call |
| `api_contracts_v2.md` | Expected I/O contracts for planning |
| `data_flow_master_v2.md` | Planner and memory flow references |

### 📝 Notes to Development Team
- Planner should be modular to support tool addition without code rewrites.
- Snapshots should serialize full in-flight states in minimal YAML.
- Memory sync must support both live LLM calls and offline replays.

---

### 🧠 Planner + Memory Example

Imagine a user asks PolicyGPT to generate a rationale for "Gate 2 – Impact Assessment."

1. **Planner Role (`planner_orchestrator.py`):**
   - Breaks the request into subtasks:
     - Gather context from prior gates
     - Retrieve evidence or citations
     - Expand and draft the rationale section
     - Validate quality and flag gaps
   - Assigns each subtask to tools and orders their execution.
   - Tracks completion and passes intermediate outputs to the next step.

2. **Memory Sync (`memory_sync.py`):**
   - Saves tool inputs/outputs for each subtask into `PromptLog`.
   - Stores structured YAML traces that can be exported or reused.
   - Ensures the planner can "rehydrate" in case of session loss.

3. **Session Snapshot (`SessionSnapshot.py`):**
   - Captures full in-flight session state: which section, progress, tools used.
   - Enables seamless handoff between team members or GPT sessions.
   - Can be reloaded later to resume from exact state or audit decisions.
