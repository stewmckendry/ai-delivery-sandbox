## WP27 – Phase 1: Iteration 1 Plan

### 🎯 Objective
Create and test a minimal end-to-end experience for generating a single section of a Gate 0 artifact using both CLI and custom GPT front-end.

### 🧪 Test Scope: Generate One Section
Simulate a PM starting their artifact by generating a single section (e.g., Problem Statement) based on uploaded input and confirmed project profile.

### 🧰 Selected Tools + Toolchains
| Step | Tool/Chain | Purpose |
|------|------------|---------|
| Input Upload | `uploadTextInput` | Upload raw input for ingestion |
| Metadata Validation | `inputChecker` | Validate and tag input correctly |
| Project Context | `confirmProjectProfile` | Load the project profile for grounding |
| Generate Section | `generateSectionChain` | Draft a new section from inputs + profile |
| Review Output | Manual + Evaluation Rubric | Score output (tone, coverage, readiness) |

### 🔁 Dual Testing Modes
1. **CLI Automation**
   - `test_ingest_and_generate_section.py`
   - Uses fixed test data and prints intermediate outputs

2. **Custom GPT Front-End**
   - Hook up OpenAPI schema
   - Validate UX realism, friction, and flow

### 📄 Planned Artifacts
- `test_ingest_and_generate_section.py`
- `sample_input_text.txt`
- Evaluation rubric (Approver Confidence, Rework Estimate, Coverage)
- Feedback note with improvement suggestions

### 🗂️ Working Directory
`project/build/wps/WP27/`

### ✅ Outcome
A validated single-section journey with both backend and front-end perspectives to guide the next iteration.