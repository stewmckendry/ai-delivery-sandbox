# Planner Phase Services (Next Phase Proposal)

## Overview

This proposal outlines the next evolution of the document generation pipeline: breaking the Planner’s monolithic toolchain into **phase-based services**. These services expose key checkpoints in the generation process, enabling interaction, visibility, and traceability through GPT-led dialog while preserving backend reliability and validation.

---

## Motivation

The current pipeline executes planner tasks as backend chains (e.g., `compose_and_cite` → `validateSection` → `commitSection`) without opportunity for:
- Midpoint user interaction
- GPT-led feedback or revision
- Reuse of partial outputs or intermediate planning steps

Planner Phase Services solve this by creating discrete, callable endpoints for each stage, letting GPT (and optionally the user) pause, view, modify, or retry.

---

## Proposed Planner Phase Service Endpoints

### 1. `/tasks/prepare_drafting_context`
- **Function**: Assemble and return all available context for a given section
- **Inputs**: `section_type`, `project_id`
- **Outputs**:
  - `inputs_summary` (from PromptLog)
  - `project_profile_summary`
  - `template_outline` (from gate_reference.yaml)
  - `retrieved_evidence[]` (from KB + external sources)
  - `missing_inputs[]`
- **GPT Role**: Present summary to user, confirm intent to proceed

### 2. `/tasks/propose_draft_plan`
- **Function**: Propose a YAML-based planner sequence for drafting this section
- **Inputs**: `section_type`, `project_id`, optional `user_constraints`
- **Outputs**: `planner_task_trace.yaml`
- **GPT Role**: Review or narrate plan, propose edits if needed

### 3. `/tasks/execute_draft_phase`
- **Function**: Execute the plan and generate draft (single phase)
- **Inputs**: `plan_id`, optional `chunk_id`
- **Outputs**: `section_draft`, `reasoning_trace`, `citations`
- **GPT Role**: Show draft, ask for feedback or edits

### 4. `/tasks/validate_and_commit`
- **Function**: Validate draft structure, then save to DB and Drive
- **Inputs**: `section_markdown`, `section_type`, `project_id`, `user_id`
- **Outputs**: `validation_result`, `issues[]`, `commit_status`, `Drive_url`
- **GPT Role**: Narrate validation issues and handle user approval

---

## GPT Integration Points
- **At each phase**, GPT can:
  - Fetch and summarize outputs
  - Offer UI-based checkpoints
  - Apply user feedback to re-run plan steps
  - Trace memory and expose reasoning

---

## Deliverables to Move From Current to Proposed Model

### 1. `/tasks/prepare_drafting_context`
- **Function**: Aggregates PromptLog, project profile, and KB
- **Inputs**: `section_type`, `project_id`
- **Outputs**: All drafting context as JSON or YAML
- **Notes**: Replaces implicit planner context loading

### 2. `/tasks/propose_draft_plan`
- **Function**: Generates a structured YAML toolchain per section
- **Inputs**: `section_type`, `project_id`
- **Outputs**: `planner_task_trace.yaml`
- **Notes**: Returns tool list and parameters, editable by GPT

### 3. `/tasks/execute_draft_phase`
- **Function**: Run plan and log outputs without committing
- **Inputs**: `plan_id`, optional `chunk_id`
- **Outputs**: Markdown draft + reasoning trace
- **Notes**: Breaks apart `compose_and_cite` for GPT orchestration

### 4. `/tasks/validate_and_commit`
- **Function**: Finalize, validate, store
- **Inputs**: Draft content + trace
- **Outputs**: DB write, Drive sync
- **Notes**: Already in scope but can now be GPT-triggered

---

## Compatibility with Current Phase

This evolution **builds on** the current WP17b, WP18, and WP20:

| Phase 2 WP | Role | Phase Services Impact |
|------------|------|------------------------|
| WP17b – Section Drafting | Draft from inputs | Will decouple compose, validate, and commit |
| WP18 – Artifact Assembly | Bundle sections | No change required |
| WP20 – Google Drive | Sync and monitor edits | Compatible with commit phase |

---

## Summary
Planner Phase Services let GPT play a true co-pilot role: seeing each phase, explaining it to the user, adjusting when needed, and enforcing rigor through validation. They extend the structured benefits of planner-based drafting into a more visible, navigable process for real-time collaboration.