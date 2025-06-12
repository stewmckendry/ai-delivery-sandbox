# Task 22: Human-in-the-Loop MFA + Challenge Flow

## 🎯 Goal
Handle portal login interruptions like MFA, CAPTCHA, or security questions using a secure human-in-the-loop pattern.

## 📂 Target Files
- `app/adapters/common/challenges.py`
- Extend `orchestrator.py` to support paused sessions

## 📋 Instructions
- Detect prompts in Playwright for:
  - OTP entry, CAPTCHA images, security questions
- Pause scraper and trigger user prompt via chat (or store screenshot for UI pickup)
- Use Redis to store challenge state and await user response
- Resume Playwright session after response
- Log all steps securely, redact PHI

## 🧪 Test
- Mock challenge detection and user input flow
- Validate challenge resume and output

## ✅ What to Report Back
- Challenge handler logic
- UI or CLI mock to simulate user response
- End-to-end flow logs