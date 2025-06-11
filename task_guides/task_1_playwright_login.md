# Codex Agent Task: Playwright Login Automation (Spike)

## 🎯 Goal
Create a Playwright script to simulate user login to a mock health portal and save post-login content.

## 📂 Target File
`app/adapters/mock_portal.py`

## 📋 Instructions
- Use Python with Playwright
- Read credentials from `.env` (`MOCK_USERNAME`, `MOCK_PASSWORD`)
- Navigate to `https://mock-health-portal.dev/login`
- Log in and wait for dashboard
- Save the post-login HTML to a local file: `login_page.html`

## ✅ What to Report Back
- File path and full code
- CLI command to run the script
- Required `.env` variables
- Output artifact(s) and how to verify them
- Any assumptions or simplifications made

Refer to [review_checklist.md](review_checklist.md) for formatting.