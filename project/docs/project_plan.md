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
- ⬜ Project repo and branching structure ✅
- ⬜ Create mock portal pages for dev/testing
- ⬜ Spike: Playwright login automation (2 sample portals)
- ⬜ Spike: PDF parsing with PyMuPDF
- ⬜ Spike: HTML table extraction with BeautifulSoup
- ⬜ Spike: RAG-style GenAI prompt tuning

### Phase 2: Portal Integration
- ⬜ Build secure portal credential UI (local-only)
- ⬜ Build Playwright adapter for Portal A
- ⬜ Build Playwright adapter for Portal B
- ⬜ Extract content (HTML, PDFs)

### Phase 3: Data Processing
- ⬜ Write parser for lab results PDF
- ⬜ Write parser for visit summary HTML
- ⬜ Normalize structured data into JSON

### Phase 4: GenAI Chat & RAG
- ⬜ Create JSON-to-prompt template
- ⬜ Build chat UI (React + shadcn/ui)
- ⬜ Integrate LLM backend with RAG
- ⬜ Handle source referencing in answers

### Phase 5: Reporting
- ⬜ Create summary report formatter (Markdown → PDF)
- ⬜ Add export button to UI

### Phase 6: UX & Demo Polish
- ⬜ Basic styling (Tailwind, layout)
- ⬜ Add session privacy notice / disclaimers
- ⬜ Record walkthrough video
- ⬜ Prepare slide deck for demo

---

## 🧭 Task Management Notes
- Tasks organized by system dependencies
- Initial portal and LLM use tied to your real test accounts
- Chat output and report generation depend on successful data structuring

This plan will evolve as we build and learn. Status will be updated inline.