# Codex Agent Task: Portal A Adapter (Scraper)

## 🎯 Goal
Use Playwright to log in to a health portal and download sample content.

## 📂 Target File
- `app/adapters/portal_a.py`

## 📋 Instructions
- Use Playwright in headless mode
- Accept login credentials as arguments
- Navigate to mock portal URL
- Log in using `input[name='username']`, `input[name='password']`, `button[type='submit']`
- After login:
  - Extract and save dashboard HTML to `/tmp/portal_a_dashboard.html`
  - Download max 3 PDF links to `/tmp/`
- Return a list of saved file paths and summary metadata

## ✅ What to Report Back
- Code file path + content
- How to run scraper (CLI or script entrypoint)
- Output files created and where
- Any assumptions (selectors, layout, URLs)

Refer to `task_guides/review_checklist.md` for format.