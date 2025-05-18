# 🧱 Ways of Working – AI-Delivery Sandbox Project (May 2025)

## 1. We Are a Team
We collaborate as one team with clear roles:
- Human Lead sets direction and priorities.
- GPT Pod proposes plans, drafts, and requests inputs.
- Human provides inputs and final approval.

### Flow
1. Human Lead: "Let's do ___ next."
2. GPT Pod: proposes plan, requests inputs.
3. Human: confirms direction or adjusts.
4. GPT Pod: generates outputs.
5. Human: reviews and approves or revises.
6. GPT Pod: commits output, continues to next step.
- Every time a file is committed, GPT will return the link to that file in Git. URL syntax: `https://github.com/stewmckendry/ai-delivery-sandbox/tree/sandbox-curious-falcon/<path_from_root>`

## 2. We Iterate Rapidly
Fast, structured drafts are followed by sharp review.
- Human clarifies goal.
- GPT generates v0.8 quickly.
- Human sharpens or redirects.
- GPT iterates rapidly, batch sizes grow.

## 3. Git Is Source of Truth
- Always fetch latest files before work.
- Work applies against latest base.
- Git-native tools are used for patching, committing, lifecycle.
- Commit outputs, not raw prompts.
- Log reasoning and decisions via chain-of-thought and task lifecycle tools.

## 4. Document Everything
- All outputs committed.
- Reasoning trace logged per task.
- Handoff notes written when continuing or scaling.
- Outputs and process docs live in `/project/`, reference copies in `/framework/`.

## 5. Continuous Learning
- Log issues and enhancements.
- Capture what worked and what didn’t.
- Use retrospectives to evolve this doc.

## 6. Repo Structure Discipline
We use a strict folder structure with versioning rules:

```
/app/                          # All code
/framework/                   # Read-only reference files
/project/
  discovery/                  # Personas, market, goals
  build/                      # Design, schemas, architecture
  test/                       # Test plans, cases, logs
  system_design/              # Global design docs (see list below)
  outputs/                    # Task outputs + logs
  research/                   # Spikes, exploration, one-off studies
  reference/                  # YAMLs or structured domain/process models used by the app
memory.yaml                   # File index with tags
task.yaml                     # Task definitions
changelog.yaml                # File-level change log
requirements.txt, .gitignore  # System files
```

> Every pod will work in:
> - repo_name: `ai-delivery-sandbox`
> - branch: `sandbox-curious-falcon`

### System Design Folder – Versioned Artifacts
These docs are foundational and must be version-controlled:
- `system_architecture.md` – High-level overview of the app's architecture, showing how front-end, API tools, back-end systems, and GPT interact.
- `data_flow_master.md` – Canonical view of how data moves through the system from input to storage to export, covering schemas, transformations, and flows.
- `db_schema_notes.md` – Definitions and rationales for all database models and fields, including mappings from YAML and API inputs.
- `tool_catalog.md` – Master list of all OpenAPI tools, including input/output specs, intended usage, and linkage to system behaviors.
- `api_contracts.md` – Detailed OpenAPI schemas, validation rules, and call formats used for server and GPT tool integration.
- `integration_points.md` – Map of where and how system components connect: GPT ↔ API ↔ DB ↔ external services.
- `error_handling_matrix.md` – Expected error states and how each layer (GPT, API, DB) should handle and escalate them.
- `session_memory_model.md` – Design of memory scope, fallback behavior, and how context is maintained across user sessions.
- `reference_model.md` – Domain process map: what the app is trying to do conceptually, including phases, states, and transitions.

Each should follow this structure:
```
/system_design/
  <topic>/
    v1.md
    v2.md
    addendums/<archived_or_superseded>.md or <topic_specific>.md
```

### Folder Structure Improvements (from retros):
- **Versioned folders**: For evolving docs, name versions explicitly (e.g. `data_flow/v1.md`, `v2.md`).
- **Addendums Usage**: The `addendums/` folder may serve two purposes:
  1. Archived versions that are no longer active, noted in the new file's header (e.g., `Replaces: v1.md, archived in addendums/clarification.md`).
  2. Topic-specific supplements that remain valid and expand on a section of the main doc without replacing it (e.g., `addendums/tool_input_handling.md`).
- **Use `memory.yaml`**: Every committed file is indexed with a `feature`, `phase`, and `type` tag. Run `/system/query_memory/ mode=summary` to list all artifacts by tag.

## 7. Minimize Context Creep
- Reset assumptions when needed.
- Scale out to a new pod if scope overloads.
- **Save snapshots**: Before changing phase or branching context, the outgoing pod drafts a plain-text handoff message. Include:
  - Goal and scope summary
  - Task status
  - Key decisions
  - Reference file paths
  - Repo + branch
  - Next steps and suggested prompt
- The Human Lead curates this message and sends it to the next pod.
- **Process Improvement**: Commit the handoff note to `/project/outputs/<task_id>/handoff_note.md`. To reduce manual file curation:
  - Include key file references in memory.yaml with `handoff` tag.
  - Log final state in the reasoning trace.
  - Use standard file reference format in notes to enable later automation.

## 8. Reflect and Close the Loop
- Each task logs a reasoning trace.
- GPT recommends next steps.
- Lessons and handoffs are logged.

---

## ♻️ Retrospective-Informed Additions
**New in This Project (based on retros):**
- **Versioned folders**: Implemented to avoid file sprawl (from `framework_assessment`, `framework_improvement_plan`). Every major doc gets a `v1.md`, `v2.md`, and optional `addendums/` folder for partial updates or archiving.
- **Structured pod handoffs**: Replace unused tool with curated handoff message. Commit it under `/outputs/`. Reference files using memory tags or links in reasoning trace (`return_to_play_redesign`, `qa_schema_impl_retro`).
- **Front-load user journeys**: Require each discovery task to include `user_journey_flows.md` before schema or tool design begins (`feature_2_symptom_logging_stage_inference`).
- **Test + deploy expectations upfront**: Each feature plan must include `test_symptom_stage_tools.py`, and a `deploy_guide.md` with staging steps (`framework_improvement_plan`, `qa_schema_impl_retro`).
- **Link YAML ↔ DB clearly**: Design phase tasks must pair `reference_model.yaml` with `db_schema_notes.md` and integration notes (`data_flow_and_deployment_retrospective`).

---

This document defines our starting point. We will evolve it through future reflections, commits, and human-GPT collaboration.