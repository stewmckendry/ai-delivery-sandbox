# Task 24: AI-Powered Traversal and Link Filtering

## 🎯 Goal
Enable the scraper to explore portal links intelligently, prioritizing content-rich pages using LLM or heuristic scoring.

## 📂 Target File
- `app/crawler.py`

## 📋 Instructions
- After login, extract all internal links from the page
- Score each link by:
  - Anchor text (e.g. "Lab Results", "Download")
  - URL path pattern (e.g. "/lab", ".pdf")
  - Optional: use LLM to classify link usefulness
- Maintain queue of URLs to visit (limit by depth or count)
- Skip revisited links (use a set of visited URLs)
- Return a list of visited and saved pages

## 🧪 Test
- Unit test with fake HTML content and sample link queue
- Validate prioritization and visited logic

## ✅ What to Report Back
- Crawler logic
- Sample link score function
- Queue output and visited set

Refer to `review_checklist.md` for structure.