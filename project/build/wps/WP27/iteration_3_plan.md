## 🚀 WP27 – Iteration 3 Plan: Section Loop + Document Assembly

### 🎯 Objective
Enable end-to-end artifact drafting from user upload to assembled document by expanding the toolchain to:
- Loop through all required sections
- Apply global research once
- Maintain context across sections
- Assemble the final draft using `assemble_artifact_chain`

---

### 📘 Building on Iteration 2
- We now have a reliable `generate_section_chain` for single-section generation.
- LLM prompt templates are correctly hydrated.
- Clean logs and validated end-to-end flow with reasoning trace.

---

### 👤 Human-in-the-Loop Checkpoints
| Step | GPT / User | Role |
|------|------------|------|
| After upload | GPT | Generates project profile + checks intents |
| After each section draft | User | Reviews / adds feedback via GPT |
| After document draft | User | Final review before submission |

---

### 🔁 Section Loop Logic
We will iterate across all required `section_id`s for a given artifact, invoking `generate_section_chain` per section.

Refactor needed:
- Extract global search calls (corpus, web, alignment) outside the section loop.
- Inject `global_context` as reusable memory in each section prompt.
- Chain sections using prior outputs + section-specific intents.

---

### 🛠 Tool & Chain Use
| Tool/Chain | Role |
|------------|------|
| `upload*Input` | Upload + project profile |
| `generate_section_chain` | Generate each section |
| `assemble_artifact_chain` | Stitch sections into full document |

Enhancements:
- `generate_section_chain.py`: Split global search from section logic.
- `section_synthesizer.py`: Accept context from previous sections + global.
- New chain: `generate_artifact_chain.py` to control loop + assembly.

---

### 🧩 Patch Breakdown
1. **Refactor** `generate_section_chain` to isolate global search.
2. **Create** `generate_artifact_chain.py` to:
   - Call global research tools once
   - Loop through `sections` in reference YAML
   - Accumulate drafts and pass to `assemble_artifact_chain`
3. **Enhance** prompts:
   - Add `global_context` and `prior_sections` placeholders
4. **Update** test script for full document generation.

---

### 🧪 Testing Plan
#### 🔬 Local
- Use expanded `test_ingest_and_generate_document.py`
- Simulate multi-section loop
- Validate outputs + reasoning trace

#### 🤖 GPT Integration
- Insert GPT checkpoints after each section
- Validate user review + instruction loop

---

### 🤝 Pod Workflow
| Step | You | ProductPod |
|------|-----|------------|
| Manual patches | ✅ | Propose diffs only |
| Testing | ✅ | Validate logs, trace, and bugs |
| Prompt tuning | Collaborative | Generate YAML, adjust based on test |

---

### ⚠ Confidence Assessment & De-risking Plan

#### 🟡 Section Loop & Context Passing
- Risk: Prompt overload, repetition, weak coherence
- Plan:
  - Design prompt contract for sections
  - Dry run 2-3 section generations
  - Add summarization utility for prior sections
  - Enforce scoped global context injection

#### 🟡 GPT Checkpoints for Feedback
- Risk: User fatigue, unclear response capture
- Plan:
  - Simulate review dialog manually
  - Define interaction and feedback schema
  - Option to skip/collapse reviews

---

These de-risking steps will ensure robust design before implementation.