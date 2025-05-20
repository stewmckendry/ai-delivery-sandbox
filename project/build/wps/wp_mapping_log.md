## 🧩 Work Package Mapping Log

> Phase 1 – Input Mapping (Discovery Files)
> This log is append-only. Each entry maps discovery artifacts to proposed deliverables and work packages. Format:
> - WP ID
> - Deliverables (file paths)
> - Source file reference (path + title/snippet)

---

### 🔹 From `project_goals.md`

**Mapped to WP1 – Policy Artifact Generator**
- `app/templates/gate_document_template.yaml` – from "Project Gating Process" section
- `app/tools/structured_drafter.py` – from "Generate and commit large documents"
- `app/db/models/chain_of_thought.py` – from "Ensure traceability and transparency"
- `app/db/models/validation_checks.py` – from "Add validation tools"
- `app/tools/evidence_prompt.py` – from "Evidence-Based Decision Support"
- `app/tools/raci_scaffold_generator.py` – from "Governance Documentation"
- `app/tools/risk_section_filler.py` – from "Risk, Security, and Privacy Assessments"
- `app/tools/redaction_flagger.py` – from "Political Sensitivities and Cabinet Confidence"
- `app/tools/dual_language_exporter.py` – from "Bilingual Requirements"

**Mapped to WP6 – Review Workflow Routing Layer**
- `app/tools/review_router.py` – from "Interdepartmental Alignment"
- `app/db/models/review_routing_log.py` – from "Interdepartmental Alignment"

**Mapped to WP10 – Export and Translation Layer**
- `app/tools/version_exporter.py` – from "Version Control and Approvals History"
- `app/db/models/approval_signature.py` – from "Version Control and Approvals History"

---

### 🔹 From `policygpt_user_journeys.md`

**Mapped to WP1 – Policy Artifact Generator**
- `app/tools/input_chunker.py` – from Journey A step 4
- `app/tools/section_synthesizer.py` – from Journey A step 4
- `app/tools/outline_drafter.py` – from Journey A step 4
- `app/tools/content_integrator.py` – from Journey A step 7
- `app/tools/preview_renderer.py` – from Journey A step 8
- `app/db/models/project_profile.py` – from Journey A step 4 (metadata coherence)
- `app/tools/yaml_metadata_attacher.py` – from Journey A step 4 (commit with metadata)

**Mapped to WP11 – Document Feedback and Diff Engine**
- `app/tools/feedback_ingester.py` – from Journey C step 1
- `app/tools/section_comparator.py` – from Journey C step 3
- `app/tools/highlight_differ.py` – from Journey C step 3

**Mapped to WP3 – Toolchain Integration Layer**
- `app/engines/section_stitcher.py` – from Journey A step 7
- `app/tools/tool_config_loader.py` – from "Technical Enhancements: Reference Files"

**Mapped to WP8 – Evidence and Citation Tool**
- `app/tools/justification_prompt.py` – from "Evidence-Based Checks"

**Mapped to WP4 – Gating Doc Quality Engine**
- `app/tools/quality_checker.py` – from "Input Guidance" + "Validation Tools"

**Mapped to WP2 – Document Commit + Audit Logging**
- `app/db/models/version_metadata.py` – from "Audit and Metadata"

---

✅ More mappings to be appended as system_design files are processed.

Next expected source files: acceptance criteria, tool catalog, api contracts.