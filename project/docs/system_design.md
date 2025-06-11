# System Design: Patient-Centered Health Data Co-Pilot

## 🧱 Architecture Overview

```
[User] → [ChatGPT (MCP Plugin)]
      → [FastAPI Backend (Railway-hosted)]
          → [Auth UI (for portal credentials)]
          → [Portal Adapters (Scrapers)]
          → [Raw Document Store (local/blob)]
          → [Data Processor (LLM-assisted)]
          → [Structured DB (SQLAlchemy + SQLite/Postgres)]
          → [Prompt Orchestration (YAML)]
```

---

## ⚙️ Technology Stack

| Layer        | Tech                            |
|--------------|----------------------------------|
| UI Layer     | ChatGPT + MCP Plugin            |
| Auth UI      | React (minimal)                 |
| Backend      | FastAPI (hosted on Railway)     |
| Scraping     | Playwright (headless, secure)   |
| Parsing      | PyMuPDF, BeautifulSoup          |
| Storage      | SQLAlchemy + SQLite → Postgres  |
| Temp Store   | Redis (for session state)       |
| Prompting    | YAML-configured templates       |
| GenAI        | OpenAI or Claude (via API)      |

---

## 🔐 Credential Input Flow
- ChatGPT initiates backend request
- FastAPI issues a one-time HTTPS link to a `/auth` form
- User enters portal credentials securely
- Credentials stored encrypted (Vault/local secure storage)

---

## 🧩 Interfaces

### Portal Adapter
- Headless login (Playwright)
- HTML/PDF scraper
- Outputs raw docs + HTML snapshots

### Data Processor
- Uses LLM + NLP to clean and structure data
- Normalizes into JSON model stored in DB

### Prompt Orchestrator
- Loads `.yaml` templates per use case
- Injects structured data into RAG prompts
- Handles summarization, comparison, glossary gen

---

## 🗃 Data Models
- **Event** (date, type, provider, source, metadata)
- **LabResult** (test name, value, reference, units)
- **VisitSummary** (doctor, notes, diagnoses)

Stored using **SQLAlchemy** and **SQLite (PoC)**

---

## 📦 Dependencies
- FastAPI, Playwright, SQLAlchemy, PyMuPDF, BeautifulSoup
- Redis (optional)
- OpenAI / Claude SDKs
- Railway deployment config

---

This design emphasizes secure user control, modular adapters, LLM-powered reasoning, and extensibility into future integrations.