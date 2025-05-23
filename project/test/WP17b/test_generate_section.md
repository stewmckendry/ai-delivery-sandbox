# 🧪 WP17b Test Plan – Toolchain: generate_section

## ✅ Objective
Validate the `generate_section` toolchain flow using:
- `memory_retrieve`
- `section_synthesizer`
- `section_refiner`

Ensure the chain correctly retrieves PromptLog inputs, drafts a section, and refines it using OpenAI's API.

---

## 🛠️ Setup
### 🔹 Pre-Step: Seed PromptLog
Since upload tools do not yet populate `full_input_path` with artifact/section metadata, we manually insert test entries:

```sql
INSERT INTO prompt_logs (
    id, tool, input_summary, output_summary,
    full_input_path, full_output_path,
    session_id, user_id, timestamp
)
VALUES
(
    NEWID(),
    'uploadTextInput',
    'Problem summary input',
    'Captured user input on problem statement',
    '{
        "input": {
            "gate": 0,
            "artifact": "investment_proposal_concept",
            "section": "problem_statement",
            "intent": "describe_problem",
            "answer": "Public transit ridership has declined due to unreliable schedules and aging infrastructure."
        }
    }',
    '{}',
    'test-session-001',
    'test-user-001',
    GETDATE()
),
(
    NEWID(),
    'uploadFileInput',
    'Stats from regional review',
    'User uploaded data on transit gaps',
    '{
        "input": {
            "gate": 0,
            "artifact": "investment_proposal_concept",
            "section": "problem_statement",
            "intent": "evidence_upload",
            "answer": "Recent survey shows 40% rider drop from 2019 to 2023 in Metro Region."
        }
    }',
    '{}',
    'test-session-001',
    'test-user-001',
    GETDATE()
);
```

---

## ▶️ Test Script: `test_generate_section.py`
```python
from app.engines.planner_orchestrator import PlannerOrchestrator

if __name__ == "__main__":
    planner = PlannerOrchestrator()
    output = planner.run(
        intent="generate_section",
        inputs={
            "artifact": "investment_proposal_concept",
            "section": "problem_statement",
            "session_id": "test-session-001",
            "user_id": "test-user-001"
        }
    )

    print("✅ Final Output:\n")
    print(output["final_output"]["refined_draft"])

    print("\n📜 Trace:\n")
    for step in output["trace"]:
        print(f"{step['tool']}: {list(step['output'].keys())}")
```

---

## 📌 Expected Results
- Synthesized draft from OpenAI using both inputs
- Refined version with clearer tone
- Trace with all tools invoked successfully

---

## 🔍 Next Step
Human Lead runs test and reports back to ProductPod for results capture and commit.

---

## 📝 Notes
- Toolchain execution is handled by `GenerateSectionChain`
- Planner delegates based on intent
- PromptLog input filtering logic will need upstream population in future WPs