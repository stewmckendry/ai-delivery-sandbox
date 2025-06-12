# Codex Agent Task: Dev Seed & Preview Tool

## 🎯 Goal
Enable easy seeding of mock data and preview of summaries or Q&A in the local dev environment.

## 📂 Target File
- `scripts/dev_seed_and_preview.py`

## 📋 Instructions
- Accept CLI args (or interactive input) for:
  - Which sample file to use
  - Seed lab/visit data into DB
  - Preview `summarize_lab_results()` output
  - Preview `POST /ask` response
- Print formatted outputs to console

## 🧪 Test
- Manual run only, no unit test needed
- Ensure script prints summary + answer clearly

## 🔄 Reuse
- Summarizer from `app/prompts/summarizer.py`
- RAG API from `app/api/rag.py`
- DB models from `app/storage/models.py`

## ✅ What to Report Back
- Script and sample preview output for lab + visit inputs
- Any setup steps needed for env/DB

Refer to `task_guides/review_checklist.md` for structure.