## Reference Model (v2 - Planner-Integrated)

This file defines how PolicyGPT uses reference structures and gate requirements to drive tool planning, validation, and trace-linked drafting.

---

### 🎯 Source: `gate_reference.yaml`

* **Artifacts:** e.g., Business Case, Project Charter
* **Gates:** Gate 0 → Gate 5
* **For each gate:** lists required artifacts, and within each artifact, required sections with:

  * `required_fields`
  * `guidance`
  * `section_type`
  * `example_id` (links to approved "gold star" examples stored externally)
  * `template_id` (links to external markdown/YAML scaffold)

These IDs point to large content stored in separate files (e.g., `examples/{artifact}_{section}.md`, `templates/{artifact}_{section}.md`) and are used by tools to:

* Instruct GPT during `composeDraft`
* Generate checklists for `validateSection`
* Recommend formats or arguments during human review

---

### 🧭 Planner Integration

* Planner reads `gate_reference.yaml` and generates `planner_task_trace.yaml`

* Each section becomes a tool chain invocation plan with steps:

  1. Search (internal, external)
  2. Draft (via `composeDraft`)
  3. Human review (optional)
  4. Validate (via `validateSection`)
  5. Commit (via `commitSection`)

* Tasks and results are logged in `reasoning_trace.yaml` with links to:

  * `PromptLog`
  * `ArtifactSection`
  * `citations`

---

### 🧩 Dynamic Tool Selection

```python
if not has_required_evidence():
    run("externalWebSearch")
elif not validator_passes():
    run("regenerate_and_validate")
elif missing_inputs():
    run("follow_up_question")
```

Planner dynamically invokes tools based on context gaps, validator feedback, and section constraints.

---

### ✅ Validated Output Requirements

Each section must:

* Fulfill required fields from `gate_reference.yaml`
* Pass structure validation (`validateSection`)
* Include traceable `reasoning_steps`
* Link to citation sources (internal and external)
* Align with templates or include reason for deviation

---

### 📎 Example Task Mapping

```yaml
planner_task_trace.yaml:
  task: Draft rationale for Gate 1
  artifact: Business Case
  gate: 1
  tool_sequence:
    - searchKnowledgeBase
    - externalWebSearch
    - composeDraft
    - validateSection
    - commitSection
  trace_link: reasoning_trace_1245.yaml
```

---

### 🛠️ Implementation Actions

* [x] Move all example and template content to external files (e.g., `examples/*.md`, `templates/*.md`)
* [ ] Replace `example_text` and `template_outline` in `gate_reference.yaml` with `example_id` and `template_id`
* [ ] Update `composeDraft` to fetch and inject example/template content based on ID
* [ ] Extend `validateSection` to enforce schema from `gate_reference.yaml`
* [ ] Enable fallback tool chaining in planner (via rule logic or scoring)
* [ ] Add UI affordance to preview and pin examples during drafting

---

This reference model ensures traceable, planner-driven output aligned with GC gating expectations and structured document integrity.
