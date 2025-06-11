# System Design: Patient-Centered Health Data Co-Pilot

## 🧱 Architecture Overview

```
[User] 
  ↓
[ChatGPT (via MCP Plugin)] ←─────────────┐
  ↓                                      │
[FastAPI Backend (Railway-hosted)]       │
  ↓                                      │
[Prompt Orchestrator (YAML)]             │
  ↓                                      │
[Structured Data Store (SQLAlchemy)]─────┘
  ↓
[Raw Document Store (PDF/HTML)]
  ↓
[Portal Adapters (Playwright Scrapers)]
  ↓
[Minimal Web UI for Auth Input]
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

## 🔁 Interaction Flow (MCP to RAG)

1. User talks to ChatGPT (MCP plugin enabled)
2. ChatGPT sends question via connector to FastAPI
3. FastAPI retrieves relevant structured data
4. Prompt orchestrator loads appropriate YAML prompt
5. Prompt is sent to LLM for grounded response
6. Response is returned to user in ChatGPT

---

## 🔐 Credential Input Flow
- ChatGPT triggers credential collection
- FastAPI generates a secure one-time link
- User visits link and enters credentials (secure form)
- Credentials stored encrypted and scoped to session

---

## 📦 Core Dependencies
FastAPI, Playwright, SQLAlchemy, PyMuPDF, Redis, OpenAI/Claude SDK, PyYAML, Railway, dotenv, BeautifulSoup

This system design now fully includes ChatGPT → MCP → FastAPI → RAG → LLM loop.