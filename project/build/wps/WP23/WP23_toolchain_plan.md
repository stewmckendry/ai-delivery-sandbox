# WP23 Toolchain Plan: revise_section_chain (v3)

## 🧠 Objective
Implement `revise_section_chain`, a toolchain that ingests user feedback, maps it to relevant artifact sections, regenerates updated content, and logs all outputs for traceability.

---

## 🧱 Components

### 1. `revise_section_chain.py`
**Purpose:** Orchestrates the flow from input to revised section and logging.

### 2. `feedback_mapper.py`
**Purpose:** Identify impacted section(s) and classify feedback type (tone, structure, content). Uses LLM.

### 3. `section_rewriter.py`
**Purpose:** Generate revised content using the correct prompt from `revision_prompts.yaml`. Uses LLM.

### 4. `feedback_preprocessor.py`
**Purpose:** Clean noisy inputs. Optional step. Uses LLM.

### 5. `manualEditSync.py`
**Purpose:** Accepts direct edits verbatim. Logs the change.

---

## 🔁 Flow Logic
1. Detect input type (feedback, uploaded revision, or chat edit)
2. (Optional) Preprocess
3. Map to sections
4. Choose revision mode (GPT rewrite or verbatim)
5. Generate and validate new content
6. Log outputs:
   - `ArtifactSection`: updated text
   - `ReasoningTrace`: chain of tools used
   - `PromptLog`: prompt and results

---

## ✅ Deliverables
(unchanged from v2)

---

## 🧪 Tests
(unchanged from v2)

---

## 🗃️ DB Usage
(unchanged from v2)

---

## 🧭 UX Integration & GPT Routing Logic
(unchanged from v2)

---

## 🔚 Exit Paths and Drive Integration

### Toolchain Output:
- `ArtifactSection`: Updated section text
- `PromptLog`: Edit input/output
- `ReasoningTrace`: Revision steps

### User Journey Paths:

#### **A. Chat-Based Revision**
- GPT performs revision
- User confirms
- Section saved to DB
- **Drive:** Manual or planner-triggered reassembly

#### **B. Uploaded Feedback / Revised File**
- Input processed + revised
- Section updated + logged
- **Drive:** User/planner can trigger `assemble_artifact_chain`

#### **C. Verbatim Edit Upload**
- `manualEditSync` logs verbatim update
- **Drive:** Same trigger path via user or planner

### Drive Sync
- Run `assemble_artifact_chain` with revised sections
- Outputs finalized doc
- Calls `storeToDrive` and logs new version in `DocumentVersionLog`

---

## 🪜 Next Steps
(unchanged from v2)

---

*Updated to include output structure, exit paths, and Drive sync flow.*