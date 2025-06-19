# 🧪 Task 319: Add Mock Data and Demo Mode for GPT Testing

## 🧠 Context
The AI Health Records Assistant is being prepared for external use. The repo is `ai-delivery-sandbox`, branch `sandbox-curious-fox`.

Not all users will want to use personal data or have Operator access. To enable frictionless testing and demo flows, we need sample data and a demo-mode option.

## 🎯 Goals
1. Provide clean, realistic health records for testing
2. Enable a drop-in session with test data (no upload required)
3. Allow the Assistant to answer real questions without needing Operator or Pro plan

## 📦 What to Build
- Add a sample PDF to `project/demo_data/`
- Add `/mock_upload` or `/load_demo_session` route that:
  - Creates a new session
  - Auto-inserts structured records from test file
  - Indexes to Chroma if available
- Ensure `/summary`, `/ask`, `/ask_vector`, and `/export` work against demo session

## 🧪 Done When
- Users can hit a single endpoint to load a test session
- GPT can respond to realistic prompts like “What do my labs show?” using this session
- Demo file is clearly marked and contains no real PHI

Let Stewart know when this is complete so it can be added to onboarding flows.