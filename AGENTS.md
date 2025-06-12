# 🤖 Codex Agent Guide: ai-delivery-sandbox

Welcome to the **Codex Agent workspace** for the AI Health Records Copilot.
This file provides metadata, naming conventions, and practices for agents contributing to this codebase.

---

## 🗂️ Repo Structure

| Folder               | Purpose                                 |
|----------------------|-----------------------------------------|
| `app/adapters/`      | Portal scrapers and authentication      |
| `app/api/`           | FastAPI routes                          |
| `app/processors/`    | HTML/PDF parsing, structuring, summarizing |
| `app/prompts/`       | Prompt templates and LLM logic          |
| `app/storage/`       | SQLite and Redis storage                |
| `tests/`             | Unit tests for each component           |
| `task_guides/`       | Task instructions and review reports    |


## 🔁 Naming Conventions

- Task prompts: `task_guides/task_<ID>_<desc>.md`
- Review reports: `task_guides/reports/task_<ID>_<desc>_report.md`
- Python modules mirror purpose: `summarizer.py`, `rag.py`, `pdf_parser.py`

## ✅ Agent Checklists

Agents should consult `task_guides/review_checklist.md` before submitting.

Each task should include:
- Input/output specification
- Test file with mocked or isolated data
- Sample output or log line
- Summary of implementation

## 📦 Requirements

Install all packages with:
```bash
pip install -r requirements.txt
playwright install
```

## 🤝 Coordination

Agents are expected to:
- Use branch: `sandbox-curious-fox`
- Commit only their assigned files
- Link work to task prompts in `task_guides/`

Thank you for contributing to this Codex-powered AI PoC 🚀