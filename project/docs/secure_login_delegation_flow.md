# Secure Login + Delegation Flow (AI Agent Portal Access)

## 🎯 Goal
Enable a GenAI agent to access user-authorized portals securely, with full user control, compliance (HIPAA/GDPR), and protection against credential misuse.

---

## 🔐 Core Flow

```text
User (ChatGPT or UI) ───▶ Consent + Credentials ───▶ Backend (FastAPI)
                                 │                            │
                                 ▼                            ▼
                            Redis (TTL)         ───▶ Playwright Browser (per session)
                                 ▲                            ▼
                User Responds to MFA/Challenge ◀── Pause + Prompt (MFA, CAPTCHA, etc)
                                 │                            │
                                 └─────── Logs + Audit ──────┘
```

---

## 🧱 Components

### 1. Consent & Audit
- `POST /consent` logs explicit user approval per portal/session
- Logged with timestamp, user ID, portal, intent

### 2. Credential Handling
- Stored securely in Redis with 10-minute TTL
- Encrypted with Fernet; never exposed to LLM
- Accessed only by orchestrator, deleted after use

### 3. Playwright Orchestration
- Detects MFA/Challenge/CAPTCHA inputs
- Pauses session and saves screenshot or text
- Waits for user input from ChatGPT or UI

### 4. Token-Based Delegation (Optional)
- Future: JWT or cookie contains session + scope metadata
- Identity-aware proxy accepts token instead of raw password
- Enables AI agent to present scoped identity securely

---

## 🧠 Design Principles
- ✋ Human-in-the-loop required for all challenges
- 🔐 Credentials never enter LLM context
- 🕓 All sessions short-lived (scrape → logout)
- 🪪 Identity and actions logged ("AI X accessed Portal Y at T")

---

## 🔄 Status
✅ Redis-backed secure credentials
✅ Session teardown + logs
🟡 MFA/Challenge handler in progress
🟡 Token-based proxy design proposed

---

## 📦 Next
- Implement `challenge.py` handler (Task 22)
- Capture screenshots, await user input in Redis
- Log every step in `audit.py`

This enables a zero-trust, user-driven portal access model for sensitive data workflows.