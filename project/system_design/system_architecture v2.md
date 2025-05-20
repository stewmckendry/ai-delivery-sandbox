## System Architecture (Enhanced)

### Overview

This document provides a high-level system architecture for PolicyGPT, updated to reflect integration of agentic planning, evidence-first drafting, validation layers, and structured reasoning trace capture—capabilities aligned with ChatGPT's Deep Research mode.

---

## Architecture Layers and Components

### 1. UI/UX Layer

**Tech:** Custom GPT (OpenAI) + File Uploads

* **Function:** User-facing interface for writing, reviewing, and managing gate documents.
* **Enhancements:**

  * Canvas + Google Docs round-trip edits
  * Visual prompt planner previews
  * GPT assistant modes: Compose, Refactor, Explain, Validate
  * Output previews with trace highlights

### 2. Agentic Planner Layer

**Tech:** GPT + YAML + FastAPI planner tools

* **Function:** Decomposes project goals and gate requirements into sequenced tasks
* **Inputs:** `project.yaml`, `gate_reference.yaml`
* **Outputs:** `reasoning_trace.yaml`, `planner_log`, task plans
* **Enhancements:**

  * Generates `section_plan` per gate
  * Auto-triggers toolchains (`compose_and_cite`)
  * Tracks cross-section narrative linkage

### 3. Tool Backend (FastAPI)

**Tech:** Python + FastAPI + OpenAPI Tools

* **Function:** Tool routing, chunking, and validator gating
* **Enhancements:**

  * `validate_section`, `log_reasoning_trace`, `compose_and_cite`
  * Token-aware rerouting and retry fallbacks
  * Post-tool YAML state update

### 4. Validator & Trace Layer

**Tech:** Rule engine + Markdown parser

* **Function:** Applies structural, logical, and content validation rules before commit
* **Inputs:** Section markdown + YAML
* **Outputs:** Pass/fail result, validator log
* **Enhancements:**

  * Detects missing fields per `gate_reference.yaml`
  * Tracks rule hits, user override count
  * Linked to `reasoning_trace.yaml`

### 5. Knowledge Base

**Tech:** ChromaDB + sentence-transformers + externalWebSearch

* **Enhancements:**

  * Auto-triggered from planner
  * Linked citations injected inline via `compose_and_cite`
  * Fall back to external search with trust filter

### 6. Document Management

**Tech:** Google Drive API

* **Enhancements:**

  * Editable Drive mirror with trace comments
  * Validator output logs stored alongside document
  * Enhanced naming/version structure from planner metadata

### 7. Reference / Lookup Data

**Tech:** Airtable

* **Enhancements:**

  * Auto-suggest inputs from prior GC artifacts
  * Flags inconsistencies with gate-stage expectations

### 8. Reasoning Trace Capture

**Tech:** YAML + DB-backed `ReasoningTrace`

* **Enhancements:**

  * Each section commit stores reasoning log
  * Captures tool path, evidence used, validator passes
  * Serves as GPT memory input on reload

---

## Implementation Patterns

* **Prompt Design:** Generated per section with planner hooks
* **Planner Orchestration:** Uses task IDs and stage-level map
* **Commit Patterns:** Toolchain results flow into DB, YAML, Drive
* **Validation Enforcement:** Commit blocked until validator passes or override by user
* **Trace + Log Format:** YAML first, markdown preview secondary

---

## New Capabilities Alignment Table

| Capability                | Architecture Support Component                |
| ------------------------- | --------------------------------------------- |
| Agentic orchestration     | `document_orchestrator`, `planner_log`        |
| Multi-tool chaining       | `compose_and_cite`, FastAPI orchestration     |
| Quality enforcement       | `validate_section`, validator layer           |
| Reasoning trace logging   | `log_reasoning_trace`, `ReasoningTrace` table |
| Inline citation integrity | Markdown parser + evidence inject             |
| Full-document cohesion    | Planner cross-linker logic                    |

---

## Next Steps

* Integrate planning YAML hooks across tool flows
* Update backend DB with new trace + validator fields
* Create UI for planner map and validation report review
* Implement smart reroute when validator fails

This enhanced architecture positions PolicyGPT to reliably deliver high-grade documentation with deep traceability and audit readiness across all government gating stages.

---

# PATCH: System Architecture (v2.4 – Document Feedback + Approval Flow Enabled)

## 🔄 New Layer Additions and Enhancements

### 9. Feedback & Approval System

**Tech:** PostgreSQL + Planner Hooks + AuditTrail

* **Function:** Captures human feedback and formal approvals tied to document versions

* **Components:**

  * `DocumentFeedback`: stores reviewer comments linked to `ArtifactSection` or full artifact
  * `ApprovalLog`: captures Gate-level decision metadata
  * `doc_feedback_to_task`: tool that parses feedback into planner-ready tasks
  * `diff_and_summarize_sections`: highlights deltas between versions to aid review

* **Planner Integration:**

  * Feedback triggers follow-up planning
  * Approvals gate `commitDocument` operations

* **UI Support:** Reviewer dashboard with version compare + feedback resolution tracker

---

### 🧠 Memory Model Alignment

**Enhancement:** Align memory across document sessions using:

* `reasoning_trace.yaml` (YAML)
* `DocumentVersionLog` (DB)
* `DocumentDiff` (DB)
* Memory rehydration logic that detects reused `section_id` or `document_id` and loads prior planner state, validator log, and citations.

---

### 📂 Updated Implementation Patterns

* Planner recognizes unresolved feedback and injects `reviseSection` steps
* Validator blocks commit unless `ApprovalLog` present for finalized gates
* Feedback and approval logs indexed for traceability in `AuditTrail`
* Expanded UI to show full-document orchestration trace with feedback loop

---

### 📊 Architecture Support Table (Updated)

| Capability                        | Architecture Component                           |
| -------------------------------- | ------------------------------------------------ |
| Agentic orchestration            | `document_orchestrator`, `planner_log`           |
| Multi-tool chaining              | `compose_and_cite`, FastAPI orchestration        |
| Quality enforcement              | `validate_section`, validator layer              |
| Feedback loop + planning         | `DocumentFeedback`, `doc_feedback_to_task`       |
| Version diffing for reviews      | `diff_and_summarize_sections`, `DocumentDiff`    |
| Reviewer approvals and gating    | `ApprovalLog`, commit validator extensions       |
| Memory-based task reuse          | Memory rehydration logic, `reasoning_trace.yaml` |
| Document narrative cohesion      | Planner cross-linker, full-document task plan    |

---

These updates ensure PolicyGPT operates as a fully traceable, human-in-the-loop document generation system—capable of responding to reviewer feedback, supporting audit-ready approvals, and maintaining structured reasoning across iterations.
