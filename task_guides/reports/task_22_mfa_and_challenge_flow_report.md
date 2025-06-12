# Task 22 Review: Human-in-the-Loop MFA + Challenge Flow

## ✅ Summary
Implemented a Playwright + Redis challenge handling system that:
- Detects login interruptions (OTP, CAPTCHA, security questions)
- Saves a screenshot + description to Redis
- Waits for user input, then resumes the session with that response
- Fully integrated into orchestrator flow

## 📂 Files
- `app/adapters/common/challenges.py`
- `app/orchestrator.py` (updated)
- `tests/test_challenges.py`
- `tests/test_orchestrator.py` (expanded)

## 🧪 Behavior
- Challenges are returned with a `challenge_id` and `resume()` callback
- Orchestrator waits using `await_response`, then passes result to resume
- All actions are logged using audit logger

## 🔄 Detected Elements
- OTP (input[name='otp'])
- CAPTCHA (image with alt="captcha")
- Security question (input[name='security_answer'])

## ✅ Test Coverage
```bash
pytest -q tests/test_challenges.py
pytest -q tests/test_orchestrator.py
```
- ✅ Simulates user input via Redis
- ✅ Verifies that resumed sessions parse and insert content as expected

## 💬 Feedback
- ✅ Modular and easy to extend
- ✅ No assumptions about portal structure — content-agnostic
- ✅ Logs each challenge pause/resume securely

## 🚀 Production-grade flow now possible for challenge-interrupted logins