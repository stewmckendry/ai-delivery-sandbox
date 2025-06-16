# ✅ Task 202 Report: Operator Prompt Templates

## 📄 Summary
Reusable prompt templates and guidance were created to standardize how users gather health data using OpenAI Operator, ensuring data arrives cleanly for downstream ETL.

## 🔧 Implementation
- `operator_templates.md`: Prompts for Visit Summary, Labs, Billing, and All Records
- `operator_guidance.md`: Instructions on login, format (PDF preferred), naming convention, and returning to Copilot
- Format: `portal_YYYY-MM-DD_type.pdf`

## 🧪 Testing
- ✅ Prompts tested in Operator manually
- ✅ Naming convention confirmed
- ❌ Playwright not installed locally (not required for prompt-only task)
- ✅ `pytest -q` passed

## ✅ Files Changed
- `project/prompts/operator_templates.md`
- `project/docs/operator_guidance.md`

## 🏁 Outcome
Users now have actionable, reusable prompts for collecting visits, labs, billing, and exports with proper structure for reliable upload + ETL. Completes user-facing guidance for Operator integration.