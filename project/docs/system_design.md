# System Design: Patient-Centered Health Data Co-Pilot

## 🧱 Architecture Overview

```mermaid
flowchart TD
  User -->|Interacts| ChatGPT_MCP[ChatGPT (via MCP Plugin)]
  ChatGPT_MCP -->|Sends query| FastAPI[FastAPI Backend (Railway-hosted)]
  FastAPI -->|Orchestrates| PromptOrch[Prompt Orchestrator (YAML)]
  PromptOrch -->|Fetches| StructStore[Structured Data Store (SQLAlchemy)]
  StructStore -->|References| RawStore[Raw Document Store (PDF/HTML)]
  RawStore -->|Feeds| PortalAdapters[Portal Adapters (Playwright Scrapers)]
  PortalAdapters -->|Collects| AuthUI[Minimal Web UI for Auth Input]
```

---

## ⚙️ Technology Stack

| Layer        | Technology                        |
|--------------|-----------------------------------|
| UI Layer     | ChatGPT + MCP Plugin              |
| Auth UI      | React (minimal)                   |
| Backend      | FastAPI (Railway)                 |
| Scraping     | Playwright (headless, secure)     |
| Parsing      | PyMuPDF, BeautifulSoup            |
| Storage      | SQLAlchemy + SQLite → Postgres    |
| Temp Store   | Redis (session state)             |
| Prompting    | YAML-configured templates         |
| GenAI        | OpenAI or Claude (API)            |

---

## 🔁 Interaction Flow (MCP to RAG)

1. User interacts with ChatGPT (MCP plugin enabled)
2. ChatGPT sends the user's question to FastAPI
3. FastAPI retrieves relevant structured data
4. Prompt orchestrator loads the appropriate YAML prompt
5. Prompt is sent to the LLM for a grounded response
6. Response is returned to the user in ChatGPT

---

## 🔐 Credential Input Flow

- ChatGPT triggers credential collection
- FastAPI generates a secure, one-time link
- User visits the link and enters credentials (secure form)
- Credentials are encrypted and scoped to the session

---

## 📦 Core Dependencies

- FastAPI
- Playwright
- SQLAlchemy
- PyMuPDF
- Redis
- OpenAI/Claude SDK
- PyYAML
- Railway
- dotenv
- BeautifulSoup

---

## 🧩 Interfaces

**Portal Adapter**
- Headless login (Playwright)
- HTML/PDF scraping
- Outputs raw documents and HTML snapshots

**Data Processor**
- Uses LLM + NLP to clean and structure data
- Normalizes into JSON models stored in the database

**Prompt Orchestrator**
- Loads YAML templates per use case
- Injects structured data into RAG prompts
- Handles summarization, comparison, glossary generation

---

## 🗃 Data Models

- **Event:** date, type, provider, source, metadata
- **LabResult:** test name, value, reference, units
- **VisitSummary:** doctor, notes, diagnoses

Stored using SQLAlchemy and SQLite (PoC).

---

This design emphasizes secure user control, modular adapters, LLM-powered reasoning, and extensibility for future integrations.