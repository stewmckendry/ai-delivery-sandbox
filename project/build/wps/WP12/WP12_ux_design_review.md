# 🧠 UX Design Review v2: PolicyGPT Artifact Generation

## 🎯 Objective
Evaluate and enhance user experience for creating high-quality gate artifacts using PolicyGPT’s toolchains. Focus on:
- Full journey from input to document
- Procedural detail for each path
- Integration of latest WP16 and WP17b tooling
- Support for planning, feedback, and configuration
- Practical, GPT-guided execution in OpenAI Chat UI

---

## 👣 Journey A: From Scratch (PM With No Prior Inputs)

### **Goal**: Help a PM generate a high-quality gate artifact from raw project context.

### Procedure
| Step | Owner | Description | Inputs | Outputs | Dependencies |
|------|-------|-------------|--------|---------|--------------|
| 1. Trigger Input Prompting | GPT | Prompts user for context using `inputPromptGenerator` | Chat context | Input prompt | `inputPromptGenerator` |
| 2. Collect Inputs | User | Uploads notes, links, transcripts | Files, URLs, text | Uploaded content | `upload*Input` tools |
| 3. Check Inputs | Tool | GPT calls `inputChecker` to summarize coverage | Uploaded content | Coverage summary | `inputChecker` |
| 4. Confirm Gate | User | Identifies desired artifact (e.g., Risk Plan) | Gate name | Artifact requirement list | `gate_reference_v2` |
| 5. Plan Sections | GPT | Uses artifact template to enumerate sections | Gate name | Section plan | `gate_reference.yaml` |
| 6. Generate Sections | Toolchain | Runs one section via `generate_section_chain` | Memory, web, corpus | Section markdown, trace | `generate_section_chain.py` |
| 7. Review & Revise | User + GPT | Edits, reruns steps using `section_refiner` | Draft section | Updated section | - |
| 8. Assemble Doc | Toolchain | Runs `assemble_artifact_chain` to merge | Sections | Final artifact | - |
| 9. Store Output | Tool | Commits to Drive | Final doc | Drive link | `storeToDrive` |

---

## 👣 Journey B: Refining an Existing Artifact

### Procedure
| Step | Owner | Description | Inputs | Outputs | Dependencies |
|------|-------|-------------|--------|---------|--------------|
| 1. Upload Artifact or Comment | User | Uploads feedback or existing file | File, notes | Input to planner | `upload*Input` |
| 2. Locate Section | GPT + Tool | Maps input to section via embedding | Project profile | Target section | `memory_retrieve`, PromptLog |
| 3. Plan Revision | GPT | Narrates what needs update | Feedback | Action plan | - |
| 4. Run Revision Chain | Toolchain | (🔧 Needed) `revise_section_chain` executes edit | Old section, inputs | Updated draft + trace | ❌ Tool needed |
| 5. Validate & Commit | Tool | Validates and writes to DB + Drive | Revised section | Trace, file | `validateSection`, `commitSection` |

📌 **Spec Needed**: `revise_section_chain` to ingest feedback + revise section

---

## 👣 Journey C: Autopilot Mode (High-Speed PM Path)

### Procedure
| Step | Owner | Description | Inputs | Outputs | Dependencies |
|------|-------|-------------|--------|---------|--------------|
| 1. Upload Corpus | User | Bulk uploads notes, plans | Files, text | Stored memory | `upload*Input` + `index_memory` |
| 2. Trigger Full Plan | GPT | Calls composite `/tasks/generate_full_artifact` | Project + gate | Plan + sections | 🧩 Needed |
| 3. Run Full Draft | Toolchain | Iterates all sections using `generate_section_chain` | Inputs | Section drafts | ❌ Multi-section planner needed |
| 4. Assemble & Commit | Toolchain | Finalize + Drive save | Sections | Document + log | `assemble_artifact_chain` |

📌 **Spec Needed**:
- `generate_full_artifact_chain`: loops `generate_section`
- Planner that spans multiple sections

---

## 🧭 How GPT Finds Tools

GPT discovers available tools from:
- `project/reference/gpt_tools_manifest.json`: maps tool names to methods
- `project/reference/tool_catalog.yaml`: human-readable description

📌 **Enhancement Needed**: Annotate manifest with: input/output schemas, dependencies, purpose for GPT reasoning.

---

## 🔄 Roadmap for Activating UX

| Stage | User Mode | Toolchains Used | Gaps to Build |
|-------|-----------|-----------------|----------------|
| Phase 1 | Journey A (Guided Draft) | Ingest → Generate Section → Assemble | ✅ All implemented |
| Phase 2 | Journey C (Autopilot) | Full planner-run toolchain | ❌ `generate_full_artifact_chain` |
| Phase 3 | Journey B (Revisions) | Revise flow from feedback | ❌ `revise_section_chain`, feedback mapper |
| Phase 4 | Composable Planner | UI for GPT-configured planner | ❌ Planner config scaffolds |

---

## 📘 Summary

This version incorporates:
- WP16 prompting/checking tools
- WP17b corpus + alignment tools
- Enhanced journey structure
- Discovery/logging schema updates
- Phased roadmap

Let me know if you'd like visual journey flows or support with planner specs.
