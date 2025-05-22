# Prompt Schema Reference for PolicyGPT

## 📌 Purpose
PolicyGPT uses two prompt schemas:

| File | Purpose |
|------|---------|
| `prompt_block_schema.json` | Rich question metadata used by `inputPromptGenerator` |
| `prompt_schema.json` | Minimal format for logging responses in memory |

---

## 1️⃣ `prompt_block_schema.json`
- Used when generating prompts (step-by-step UX)
- Includes:
  - `question`: what GPT asks the user
  - `input_type`: type of expected input
  - `metadata`: `gate`, `artifact`, `section`, `intent`
  - `hints`: optional examples
  - `answer`: user input (optional at time of creation)

**Used by:**
- `inputPromptGenerator`
- Future tools generating or previewing prompts

---

## 2️⃣ `prompt_schema.json`
- Used to validate or organize user responses
- Key fields: `gate_id`, `artifact_id`, `section_id`, `inputs`

**Used by:**
- `inputChecker` (now)
- `compose_and_cite`, `review_and_reflect` (planned)

---

## 🧠 Integration Notes
- Tools may start with `prompt_block`, and convert to `prompt_schema` after user input
- All prompt logs should include metadata to support filtering + drafting

---

## 📂 Locations
- `project/reference/prompt_block_schema.json`
- `project/reference/prompt_schema.json`

Owner: WP16Pod