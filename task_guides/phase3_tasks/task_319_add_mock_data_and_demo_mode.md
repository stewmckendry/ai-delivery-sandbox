# 🔪 Task 319: Add Mock Data and Demo Mode for GPT Testing

## 🧠 Context
The AI Health Records Assistant is being prepared for external use. The repo is `ai-delivery-sandbox`, branch `sandbox-curious-fox`.

Not all users will want to use personal data or have Operator access. To enable frictionless testing and demo flows, we need sample data and a demo-mode option.

## 🌟 Goals
1. Provide clean, realistic health records for testing
2. Enable a drop-in session with test data (no upload required)
3. Allow the Assistant to answer real questions without needing Operator or Pro plan

## 📆 What to Build
- Add a directory of sample PDFs to `project/demo_data/`, each reflecting a different real-world context:
  - e.g., family doctor visit, hospital ER note, lab results, pharmacy list, physio summary

- Add a route `/load_demo` that:
  - Randomly selects one test case
  - Loads the file into blob
  - Creates a unique `session_key` (UUID)
  - Parses and indexes content using `run_etl_from_blob`
  - Returns:
    ```json
    {
      "session_key": "<uuid>",
      "source": "family_doctor_summary.pdf",
      "source_url": "https://...blob-link..."
    }
    ```
  - This lets GPT or users:
    - Know the correct session to use
    - View the document that was processed

- Store content under this `session_key` so it's searchable in `/ask_vector`, `summary`, etc.
- No need for advanced protections on session_key — UUID provides sufficient entropy to avoid collision.

## 🕊 Bonus
- Update `project/docs/prompt_starter_kit.md` with prompts tailored to each test case (e.g., questions about labs, medications, diagnosis)
- Update OpenAPI schema to include `/load_demo` with example response

## 🕺 Done When
- Users can trigger demo mode and immediately test GPT using realistic records
- Session-scoped data is visible across endpoints
- Demo record is viewable
- GPT has example prompts and tools to use it effectively

Let Stewart know when this is done so he can verify usability and link it into onboarding flows.