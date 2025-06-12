# Codex Agent Task: Portal B Adapter (Scraper)

## 🎯 Goal
Build a Playwright scraper for a second health portal layout.

## 📂 Target File
- `app/adapters/portal_b.py`

## 📋 Instructions
- Use Playwright
- Function accepts login credentials and portal URL
- Use alternate layout assumptions:
  - e.g., `#username`, `#password`, `button.login-btn`
- Log in and scrape post-login content
- Download up to 3 PDFs (or relevant documents)
- Save files to `/tmp/`, return file paths + metadata

## ✅ What to Report Back
- File and function(s) implemented
- How to run scraper
- Saved output examples
- Assumptions about page structure, login flow, etc.

Refer to `task_guides/review_checklist.md` for structure.