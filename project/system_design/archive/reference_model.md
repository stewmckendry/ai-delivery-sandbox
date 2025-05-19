---

## title: Reference Model

## Overview

This reference model defines the core conceptual framework underlying PolicyGPT's artifact generation lifecycle. It describes how gates, artifacts, transitions, conditions, and metadata are structured and evaluated in the system. This model is anchored in the canonical `gate_reference.yaml` file and supports tool orchestration, prompt engineering, validation, and user interface logic.

---

## Lifecycle Phases and Gate Transitions

Each GC project passes through defined "gates" (e.g., Gate 0 to Gate 6), each requiring specific artifacts. This gate-based lifecycle aligns with Treasury Board Secretariat expectations and departmental project management frameworks.

**Gate States:**
- G0: Concept Summary
- G1: Project Charter
- G2: Feasibility/Preliminary Plan
- G3: Detailed Planning/Investment Approval
- G4: Execution/Monitoring
- G5: Closeout/Transition
- G6: Evaluation/Benefits Realization

**Transitions:**
- Sequential (G0 → G1 → G2 → ... → G6)
- Conditional (some gates may be skipped, merged, or iterated based on project size/type)
- State change triggered by document approval + reviewer sign-off

---

## Artifact Structure

Each gate defines a list of required or optional artifacts. Each artifact has the following metadata:

```yaml
- gate: G1
  artifact_id: project_charter
  name: Project Charter
  sections:
    - id: rationale
      name: Rationale
    - id: scope
      name: Project Scope
  mandatory: true
  reviewer_roles:
    - Director
    - Policy Lead
  templates:
    - project_charter_template.docx
  reference_prompts:
    - rationale_prompt.yaml
    - scope_prompt.yaml
```

---

## Metadata Dimensions

Artifacts are governed by the following metadata layers:

- **Gate**: Controls visibility, sequencing, and validation logic.
- **Artifact ID**: Globally unique key for lookup and GPT orchestration.
- **Section IDs**: Used to chunk documents and manage GPT memory.
- **Reviewer Roles**: Triggers conditional prompt inclusion and approval routing.
- **Templates**: Pulled as reference documents by `fetch_reference_templates()`
- **Reference Prompts**: Used by GPT to guide drafting and validations.

---

## Usage in System

**1. Tool Catalog Integration**
- `commitSection`: Annotates metadata (section_id, gate_id, artifact_id) per commit.
- `fetchArtifactReference`: Loads template and prompt references from YAML.
- `validateArtifact`: Applies checklist-style rules from gate metadata.

**2. Prompt Engineering**
- Each section can use a specific `*.prompt.yaml` template.
- Roles such as "Director" and "Policy Lead" trigger added sections for governance, risk, or approvals.

**3. User Journey Alignment**
- Journey A (Structured Iteration): Prompts user for missing sections based on artifact map.
- Journey B (Generate All): Loops through artifact map and drafts all mandatory sections.
- Journey C (Feedback & Revise): Uses artifact ID to locate and reprocess feedback.

**4. Validation Checks**
- Gate completeness = All mandatory artifacts committed.
- Artifact completeness = All required sections present and filled.
- Metadata required for commit: gate_id, artifact_id, section_id, reviewer_role, status

---

## Gate Reference Access Pattern

```python
def get_required_artifacts(gate_id):
    reference = load_yaml("gate_reference.yaml")
    return [a for a in reference if a["gate"] == gate_id and a["mandatory"]]

# Used in: checklist generation, prompt tuning, UI onboarding
```

---

## Risks and Constraints

| Risk                              | Mitigation                                     |
|-----------------------------------|-------------------------------------------------|
| Incomplete artifact metadata      | YAML validation and schema enforcement         |
| Gate logic divergence             | Centralize transitions and version in one file |
| Reviewer routing inconsistency   | Embed roles + routing logic in reference model |

---

## Recommendation: Artifact Coverage Validator

Add a `validate_artifact_completeness(artifact_id)` endpoint to ensure all required sections, prompts, and templates exist for given artifacts.

---

## Alignment Summary

| Design Layer         | Aligned Features                                            |
|----------------------|-------------------------------------------------------------|
| Tool Catalog         | commitSection, fetchTemplates, validateArtifact             |
| User Journeys        | Journey A (iterative), B (bulk), C (revise)                 |
| Acceptance Criteria  | Section tracking, metadata labeling, reviewer integration   |
| System Architecture  | Artifact YAML used in prompt layer + validation workflows   |

---