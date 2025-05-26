# 🧠 UX Design Review: E2E Artifact Generation with PolicyGPT Toolchains

## 🎯 Objective
Evaluate current tooling and propose optimized user journeys for producing high-quality gate artifacts aligned to `gate_reference_v2`. Cover full lifecycle from input ingestion to draft assembly. Ensure experience is natural, guided, and audit-ready for PM users.

---

## ✅ Summary of Findings

PolicyGPT’s toolchains (Ingest → Generate Section → Assemble Artifact) provide strong modular support for gate document creation. We can enhance usability by designing for multiple user modes:
- From-scratch drafting
- Iterative refinement
- Full-document assembly

Key UX needs:
- Human+AI collaboration balance
- Project-aware guidance
- Transparency on toolchain actions
- Flexibility for check-the-box vs deep-editing users

---

## 👣 User Journey A: From Scratch (Guided PM Path)

### Step-by-Step
| Step | User Does | GPT Does | Tools Triggered |
|------|-----------|----------|------------------|
| 1. Select Gate | Chooses gate from dropdown | Looks up required artifacts | `gate_reference.yaml` |
| 2. Provide Inputs | Uploads docs, links, text | Extracts, summarizes | `IngestInputChain`, `upload*` tools |
| 3. Confirm Start | Clicks "Begin Draft" | Plans sections | Planner calls `generate_section_chain` |
| 4. Section Drafting | Waits, reviews each section | Summarizes memory, drafts, refines | `memory_retrieve`, `section_synthesizer`, `section_refiner` |
| 5. Revise | Suggests changes or edits draft | Rewrites and revalidates | `section_refiner`, optionally `validateSection` |
| 6. Final Assembly | Clicks "Assemble Document" | Compiles sections | `assemble_artifact_chain` |
| 7. Approve | Clicks "Commit to Drive" | Uploads to Drive | `storeToDrive` |

### Outputs
- Draft sections in DB and Drive
- ReasoningTrace for each step
- Document metadata with trace, gate, version

---

## 👣 User Journey B: Revise Existing Artifact

| Step | User Does | GPT/Tools | Notes |
|------|-----------|-----------|-------|
| Upload artifact or feedback | Uploads file or comments | `uploadFileInput` or `uploadTextInput` | Tied to `project_id` + `section` |
| Detect overlap | GPT maps inputs to existing sections | Planner uses memory context | Triggers `revise_section` if edit required |
| Confirm update | Clicks accept/revise | Saves revised section | Triggers validation + `commitSection` |

---

## 👣 User Journey C: Fast Track Mode (Autopilot)

| Step | User Does | GPT/Tools | Notes |
|------|-----------|-----------|-------|
| Upload all inputs | Uploads transcript, plans, notes | `IngestInputChain` | 
| Click “Generate Full Document” | Starts full artifact generation | Runs all toolchains sequentially | From `memory_retrieve` to `storeToDrive` |
| Receive summary link | Sees Drive link + section logs | Outputs version, reviewer tags | 

---

## 🔍 System Enhancements Recommended

### 1. Planner Composite Endpoints
- Add `/tasks/generate_full_artifact` and `/tasks/generate_and_commit_section`
- Streamline flows so GPT doesn’t call individual tools manually

### 2. Traceable Toolchain Summaries
- UI should display what GPT did in plain language:
  - “Reviewed 3 sources for Risk Section”
  - “Used `section_refiner` to polish tone”

### 3. Transparent Draft Confirmation
- Add draft preview window with:
  - `Sources used`
  - `Validation status`
  - `Reasoning summary`

### 4. Memory Reuse Across Sessions
- Leverage stored `PromptLog` + `ArtifactSection` across sections or reentry

### 5. Better Input Guidance
- Add tooltips or suggestions:
  - “Try uploading transcripts or plans”
  - “Label your inputs with artifact/section”

---

## 🔚 Conclusion
PolicyGPT has all core building blocks for powerful, user-aligned document drafting. These journey-focused enhancements will:
- Improve usability for PMs
- Increase transparency and confidence
- Enable both fast and deep-edit flows

Well-scaffolded UX + automated quality pipelines = high-impact gate artifact generation.
