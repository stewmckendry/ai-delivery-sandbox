### WP23 Test Plan: Artifact Revision Toolchain

#### ✅ Objective
Validate functionality of each tool in the `revise_section_chain` and the overall toolchain performance across key scenarios.

---

#### 🧪 Test Setup
- Ensure `OPENAI_API_KEY` is set in environment
- Load sample artifact sections into database for `artifact_id: A123`, `section_id: S1`
- Ensure prompts are available via GitHub URL as configured

---

#### 🧩 Test Scenarios and Steps

##### 1. feedback_preprocessor
- **Input**: Long raw feedback text with multiple ideas
- **Expect**: Cleaned version, type inferred, multiple split feedback items

##### 2. feedback_mapper
- **Input**: Feedback + `sections: ["S1", "S2"]`
- **Expect**: Correct section ID(s) mapped and type inferred

##### 3. section_rewriter
- **Input**: `section_id`, feedback, revision_type, current_text
- **Expect**: Revised section draft, audit trace, suggestions, and compliance check output

##### 4. manualEditSync
- **Input**: Verbatim user input with no change from current text
- **Expect**: No new version saved, log shows no change

##### 5. revision_checker
- **Input**: Original and revised text with known diff
- **Expect**: Change ratio and LLM validation feedback

##### 6. revise_section_chain end-to-end
- **Input**: Raw feedback, memory, artifact + section IDs, mode
- **Scenarios**:
  - a. `verbatim` — should store raw input directly
  - b. `rewrite` — full chain invocation, with updated artifact section
  - c. `polish` — small edit, confirm revision_checker warns on large change
  - d. `append` — text appended to existing section

---

#### 📥 Inputs
- Configured sample section in DB: `artifact_id: A123`, `section_id: S1`, `text: "This is a test section."`
- Sample feedback in test script

---

#### ✅ Expected Outputs
- Logs from each tool execution
- Saved artifact section for rewritten versions
- No-save result for verbatim with unchanged content
- Change ratio flags from compliance checker
- Trace return value with suggestions