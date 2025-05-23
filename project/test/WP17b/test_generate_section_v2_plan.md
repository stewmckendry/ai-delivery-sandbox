# ✅ WP17b Test Plan: `generate_section` Toolchain v2

## 🎯 Objective
Test enhanced version of the `generate_section` toolchain that includes:
- Output schema validation via `SectionDraftOutput`
- Paragraph chunking in `section_synthesizer` and `section_refiner`
- Storage of `draft_chunks` and version metadata in `ReasoningTrace`

---

## 🛠️ Setup Steps

### 1. Insert Dummy PromptLog Data
Create entries using a SQL insert or script to populate `prompt_logs` table:
```sql
INSERT INTO prompt_logs (
    id, tool, input_summary, output_summary, full_input_path, full_output_path, session_id, user_id, timestamp
) VALUES (
    'log-test-001', 'uploadTextInput', 'Ridership stat', 'Logged 40% drop',
    '{"input": {"gate": 0, "artifact": "investment_proposal_concept", "section": "problem_statement", "intent": "describe_problem", "answer": "Recent survey shows 40% rider drop from 2019 to 2023 in Metro Region."}}',
    '{}', 'test-session-001', 'test-user-001', CURRENT_TIMESTAMP
);
```

### 2. Environment
- Ensure `OPENAI_API_KEY` is set in `.env`
- Run from the root of the `policyGPT` repo

---

## 🚀 Test Run Steps

### Step 1: Run Toolchain
Execute test file:
```bash
python3 project/test/WP17b/test_generate_section.py
```

### Step 2: Check Output
You should see:
- ✅ Final output: Full section draft text
- 📜 Trace: Each step with `tool_version`, `schema_version`, and output keys

### Step 3: Inspect DB Tables
Check these:
- `artifact_section` → confirm full text and section metadata
- `reasoning_trace` → confirm `steps`, `draft_chunks`, `created_by`, etc.
- `prompt_logs` → confirm synthesizer/refiner log entries

---

## 🔍 Expected Results
- Section output contains coherent, complete problem statement
- Reasoning trace logs 3 steps with correct output schema
- `draft_chunks` field in DB contains 2+ paragraph segments
- Versions logged as `v1`, schema `1.0`

---

## 🗂️ Files Involved
- `project/test/WP17b/test_generate_section.py`
- `app/engines/toolchains/generate_section_chain.py`
- `app/tools/tool_wrappers/section_synthesizer.py`
- `app/tools/tool_wrappers/section_refiner.py`
- `app/schemas/section_draft_output.py`
- `app/engines/memory_sync.py`

---

## ✅ Completion Criteria
All outputs saved correctly and visible in the DB, trace is structured and versioned, output schema is valid, and test passes CLI checks.