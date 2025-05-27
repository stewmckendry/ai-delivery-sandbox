# WP23 Toolchain Plan: revise_section_chain (v2)

## 🧠 Objective
Implement `revise_section_chain`, a toolchain that ingests user feedback, maps it to relevant artifact sections, regenerates updated content, and logs all outputs for traceability.

---

## 🧱 Components

### 1. `revise_section_chain.py`
**Purpose:** Orchestrates the flow from input to revised section and logging.
- Input: comment, revised draft, or uploaded input
- Output: updated section + ReasoningTrace + PromptLog

### 2. `feedback_mapper.py`
**Purpose:** Identify impacted section(s) and classify feedback type (tone, structure, content).
- Input: feedback text or diff
- Output: section_id(s), revision_type (e.g., rewrite, polish, append)
- **Uses LLM** to perform mapping and classification.

### 3. `section_rewriter.py`
**Purpose:** Generate revised content using the correct prompt from `revision_prompts.yaml`
- Input: section_id, revision_type, memory, feedback
- Output: rewritten draft
- **LLM-powered** with scoped prompt templates to control drift.

### 4. `feedback_preprocessor.py`
**Purpose:** Clean noisy inputs, e.g., pasted comments or edits with markup.
- Optional step before mapping.
- **LLM-powered** normalization.

### 5. `manualEditSync.py`
**Purpose:** If feedback is a direct edit (e.g., user pasted new version), accept it verbatim and log edit reason.
- Supports verbatim overrides.

---

## 🔁 Flow Logic
1. **Detect input type**: user comment, upload, or direct draft edit.
2. **(Optional) Preprocess**: use `feedback_preprocessor` to clean or tag noisy input.
3. **Map to section(s)**: via `feedback_mapper`
4. **Decide edit mode**:
   - Rewrite via GPT: `section_rewriter`
   - Save as-is (verbatim): `manualEditSync`
5. **Generate + Validate**:
   - Retrieve memory: `memory_retrieve`
   - Prompt generation: `revision_prompts.yaml`
   - Apply edit with `section_rewriter`
6. **Log all outputs**:
   - Save to `ArtifactSection`
   - Log steps in `ReasoningTrace`
   - Write prompt input/output to `PromptLog`

---

## ✅ Deliverables

| File | Purpose |
|------|---------|
| `app/engines/toolchains/revise_section_chain.py` | Core orchestrator |
| `app/tools/tool_wrappers/feedback_mapper.py` | Section impact + intent detection |
| `app/tools/tool_wrappers/section_rewriter.py` | GPT editing agent |
| `app/tools/tool_wrappers/feedback_preprocessor.py` | Optional input cleaner |
| `app/tools/tool_wrappers/manualEditSync.py` | Handles direct user edits |
| `project/prompts/revision_prompts.yaml` | GPT prompt templates for edit types |
| `project/prompts/edit_trace_templates.yaml` | Template to explain edit decisions |
| `project/build/wps/WP23/WP23_edit_modes.md` | Mode decision logic (GPT vs upload) |
| `project/test/wps/WP23/test_revise_section_chain.py` | End-to-end tests |

---

## 🧪 Tests
- Feedback → correct section(s)
- Comment triggers correct prompt type
- Output preserves schema (text, sources)
- ReasoningTrace contains full tool path

---

## 🗃️ DB Usage
| Table | Use |
|-------|-----|
| `ArtifactSection` | Read/Write: Update section text |
| `PromptLog` | Log edit input/output |
| `ReasoningTrace` | Log revision chain of thought |
| `DocumentVersionLog` | (if full artifact is rebuilt) |

Past versions are preserved by version tag or prior entry archival in `ArtifactSection`. Change provenance is traceable via `ReasoningTrace.steps`.

---

## 🧭 UX Integration & GPT Routing Logic

### GPT should call `revise_section_chain` when:
- Revision is triggered by feedback, uploads, or chat edits

### GPT should call `IngestInputChain` when:
- New, untagged user content is uploaded (raw notes, transcripts, files)

### GPT should call `generate_section_chain` when:
- There is no existing draft for a section and initial generation is required

---

## 🪜 Next Steps
- Implement tool wrappers (`feedback_mapper`, `section_rewriter`)
- Build orchestrator logic in `revise_section_chain.py`
- Add logging + test file scaffolds

---

*Updated to reflect feedback mapping and routing logic clarity.*