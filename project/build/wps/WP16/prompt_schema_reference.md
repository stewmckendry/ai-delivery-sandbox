# Prompt Schema Reference for PolicyGPT

## 📌 Purpose
This schema defines the expected structure of inputs collected through PolicyGPT's guided input UX layer, organized by:
- `gate_id`: Integer referring to the current gate (see `gate_reference_v2.yaml`)
- `artifact_id`: Name of the artifact within the gate (e.g., "investment_proposal_concept")
- `section_id`: Section within the artifact (e.g., "problem_statement")
- `inputs`: Array of user-provided strings or evidence linked to that section

---

## 📂 File Location
- Path: `project/reference/prompt_schema.json`
- Format: JSON Schema
- Required fields: `gate_id`, `artifact_id`, `section_id`

---

## 🛠 Tools That Use This Schema

### ✅ Already Wired In
- **inputPromptGenerator**
  - Uses schema to fetch and format structured prompts
- **inputChecker**
  - Evaluates whether user inputs meet expected fields per gate_reference

### 🧩 Still To Be Integrated
- **compose_and_cite** (planned downstream WP)
  - Will use this schema to map draft sections to collected user inputs
- **review_and_reflect** (planned)
  - May use schema to organize feedback per section

---

## 🧠 GPT Config Notes
- GPTs using this schema should be aware of:
  - Gate + artifact context to scope questions
  - Section-specific prompting with fallback to broader questions
  - Ability to iterate and validate completeness using `inputChecker`

---

Owner: WP16Pod
Ready for use by downstream WPs.