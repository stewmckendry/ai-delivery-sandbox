## 📄 Prompt Schema Lifecycle

This document explains the purpose and usage of `prompt_schema.json`, a standard structure for collecting and managing user inputs aligned to gate artifacts in PolicyGPT.

---

### 🔧 What the Schema Represents
- A **single prompt** presented to the user
- Its expected **input type** (text, file, link, etc.)
- The **structured metadata** that links it to a specific `gate > artifact > section > intent`
- Optionally: an `answer` field once the user responds

---

### 🔄 Prompt Flow Lifecycle

#### 1. **Prompt Generation** (`inputPromptGenerator`)
- Uses `gate_reference_v2.yaml` and `triage_map.yaml` to determine what questions to ask
- Formats each as a `prompt_schema.json` object (no answer yet)

#### 2. **User Interaction**
- User is presented with these prompts
- They answer in UI or via upload
- `answer` field is filled

#### 3. **Validation** (`inputChecker`)
- Prompts with `required: true` are checked
- Any missing or vague answers may trigger clarification

#### 4. **Logging** (via Upload Tools)
- User answers are logged to `PromptLog`
- Metadata block enables retrieval by downstream tools

#### 5. **Usage in Drafting (e.g., compose_and_cite)**
- Drafting tools can query PromptLog by:
  - `gate`
  - `artifact`
  - `section`
  - `intent`
- Supports high-precision drafting, QA, and editing

---

### 📦 Where It’s Used
- `inputPromptGenerator.py`
- `uploadTextInput.py`, `uploadFileInput.py`, `uploadLinkInput.py`
- `inputChecker.py`
- Future: compose tools, QA checkers

---

### ✅ Benefits
- Consistency across modes (guided or bulk)
- Traceable inputs by document context
- Validatable by tools
- Extensible for future metadata

---