# Project Plan: Patient-Centered Health Data Co-Pilot (MVP)

## 🎯 Goal
Track all development tasks needed to deliver the MVP, sequenced by priority and system dependencies.

---

## ✅ Status Key
- ⬜ TODO
- 🔄 IN PROGRESS
- ✅ DONE

---

## 📅 Phases & Tasks

### Phase 1: Setup & Spikes
- ✅ Project repo and branching structure
- ⬜ Create mock portal pages for dev/testing
- ⬜ Spike: Playwright login automation (2 sample portals)
- ⬜ Spike: PDF parsing with PyMuPDF
- ⬜ Spike: HTML table extraction with BeautifulSoup
- ⬜ Spike: RAG-style GenAI prompt tuning (YAML format)

### Phase 2: Backend Foundation
- ⬜ FastAPI app scaffolding (host on Railway)
- ⬜ Redis setup for temp session state
- ⬜ SQLAlchemy models for health data (SQLite first)
- ⬜ Define YAML prompt templates and loader logic
- ⬜ Minimal credential input UI served via FastAPI

### Phase 3: Portal Integration
- ⬜ Build Playwright adapter for Portal A
- ⬜ Build Playwright adapter for Portal B
- ⬜ Store raw docs (PDF/HTML snapshots)

### Phase 4: Data Processing
- ⬜ Write LLM-backed data cleaning + structuring logic
- ⬜ Normalize into structured DB models
- ⬜ Create structured API endpoints (CRUD for testing)

### Phase 5: GenAI Chat + RAG
- ⬜ MCP connector to enable ChatGPT integration
- ⬜ Prompt orchestration (YAML → RAG input)
- ⬜ Handle source reference tracking

### Phase 6: Reporting + UX Polish
- ⬜ Generate user report (Markdown → PDF)
- ⬜ Add disclaimers and privacy notes
- ⬜ Record walkthrough demo
- ⬜ Prepare demo slide deck

---

## 🧭 Task Management Notes
- Reflects updated system architecture using ChatGPT UI and Railway backend
- YAML templates drive LLM interaction logic
- SQLAlchemy persists structured health data
- Redis optional for temporary session/cache

This plan evolves with the build. Status is inline editable.