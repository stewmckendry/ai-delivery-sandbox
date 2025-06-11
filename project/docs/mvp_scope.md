# MVP Scope: Patient-Centered Health Data Co-Pilot

## 🎯 Goal
Prove that an AI-native app can:
- Access real health data from user portals
- Combine it into a coherent, usable structure
- Let users ask meaningful questions about their health in natural language

## ✅ MVP Features

### 1. User Portal Integration (Real Portals, Simulated Secure Auth)
- Users input credentials for **2–3 real health portals** (provided by project owner)
- Headless browser automation (Playwright) simulates user session login
- Credentials stored securely (e.g., local .env or OS keychain in PoC)
- Auth layer designed to later support OAuth (where available)

### 2. Portal Scraping & Document Retrieval
- Scrapers for 2–3 selected health portals
- Download raw content: medical visit summaries, test results, PDFs
- Log scraping depth and structure as adapters per portal

### 3. Data Processing & Structuring
- Clean raw content using NLP + parsing tools
- Normalize data into structured JSON (e.g., events, doctors, dates)
- Handle PDFs, HTML snippets, tables with patient-readable formatting

### 4. GenAI Co-Pilot Chat Interface
- User asks questions like:
  - “What were my last test results?”
  - “Summarize my visits in 2023”
- LLM responds with references to original sources
- Retrieval-augmented generation (RAG) used for grounding answers

### 5. Summary Report Export
- Generate patient-readable report (e.g., PDF/Markdown)
- Include timeline, visits, key findings, glossary of terms

## 🧪 Technical Spikes
- Playwright auth with simulated 2FA and headless browsing
- PDF + HTML parsing (PyMuPDF, BeautifulSoup)
- JSON model for multi-portal health data
- GenAI summarization and chat tuning with safety checks

## 🚫 Out of Scope (for Now)
- Production-grade OAuth, FHIR, or full HIPAA/GDPR compliance
- Persistent storage or multi-user support
- Advanced NLP medical interpretation (e.g., diagnosis recommendations)

## 🧭 Notes
- Users remain in control of sessions and data access
- No background tasks or unauthorized scraping
- Modular auth design ensures forward compatibility with secure methods

---

This MVP is designed to prove the *value* and *feasibility* of empowering patients as the integration point for their health data using GenAI.