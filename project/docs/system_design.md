# System Design: Patient-Centered Health Data Co-Pilot

## 🧱 Architecture Overview

```
[User Device / Browser]
        ↓
[Frontend (React + Tailwind)]
        ↓
[Backend (FastAPI + Playwright)]
        ↓
[Portal Adapters (Scrapers)]
        ↓
[Document Parser (PDF/HTML → JSON)]
        ↓
[GenAI Engine (LLM + RAG)]
        ↓
[Chat Interface + Report Generator]
```

---

## ⚙️ Technology Stack

| Layer        | Tech                            |
|--------------|----------------------------------|
| Frontend     | React, Tailwind CSS, shadcn/ui  |
| Backend      | Python (FastAPI)                |
| Scraping     | Playwright (headless, secure)   |
| Parsing      | PyMuPDF, BeautifulSoup          |
| Data Layer   | In-memory JSON (PoC), SQLite    |
| AI/LLM       | OpenAI or Claude via API        |
| Auth Handling| Manual + Secure vault/local env |

---

## 🧩 Interfaces

### 1. User Auth Interface
- Input for portal URL and credentials
- Stored locally or in secure vault (never on server)

### 2. Portal Adapter (per portal)
- Login logic using Playwright
- Content scraping logic
- Output: Raw HTML, PDFs, Tables

### 3. Document Processor
- Extract data from PDFs, HTML
- Normalize to structured JSON:

```json
{
  "event_type": "Lab Result",
  "date": "2023-06-01",
  "provider": "Toronto General Hospital",
  "details": {
    "test": "Cholesterol",
    "result": "5.8 mmol/L",
    "reference": "<source URL>"
  }
}
```

### 4. GenAI Chat Interface
- Ingest structured data and documents
- RAG prompt format: context + question
- Example: "Summarize my last 3 blood tests"

---

## 🔄 Data Flow (End-to-End)
1. User logs in and enters portal credentials
2. Scraper authenticates via Playwright and downloads documents
3. Processor extracts and normalizes data into structured JSON
4. JSON data fed into GenAI prompt for summarization/chat
5. User sees answer in UI, with links to sources
6. Optionally generate report for export

---

## 📦 System Dependencies
- Playwright (browser automation)
- PyMuPDF, BeautifulSoup (parsing)
- FastAPI (backend API and tasks)
- React + Tailwind (UI)
- OpenAI / Claude (LLM APIs)
- dotenv / vault (local secrets handling)

---

This system design supports the MVP with modularity, security, and extensibility in mind.