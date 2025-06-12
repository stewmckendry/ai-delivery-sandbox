# Generalized AI-Powered Scraping Pipeline Design

## 🎯 Goal
Support login, traversal, extraction, and structuring across any healthcare portal — resilient to layout changes and rich in AI inference.

---

## 🔁 Pipeline Overview
```text
Login (UI/MFA) → Crawl → Extract → Classify → Chunk → Summarize → Store
```

---

## 🧠 AI Integration Points
- **Traversal Scoring** (Task 24): prioritize content-heavy links
- **Content Extraction** (Task 25): isolate relevant text, classify type
- **Chunking + Summarization** (Task 26): break, summarize, and dedupe

---

## 🧱 Modules
- `crawler.py`: breadth-first smart traversal
- `extractor.py`: parse HTML and tag content type
- `cleaner.py`: chunk, deduplicate, and summarize
- `classifier.py`: optional, separate type inference module

---

## 📦 Outputs
```json
{
  "type": "lab_result",
  "text": "Cholesterol: 180 mg/dL...",
  "date": "2023-05-01",
  "source_url": "https://portal/xyz"
}
```
- Ready for RAG, summary export, or FHIR transformation

---

## 🔄 Integration
- Orchestrator updates to loop through: login → crawl → extract → clean → insert
- Works with secure credential and challenge handler system

---

## 📋 Next
- Wire into existing `run_etl_for_portal()`
- Support plug-in style `crawler + extractor` flow per portal
- Extend to multi-page docs and secure message ingestion