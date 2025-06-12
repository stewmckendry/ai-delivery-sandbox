# AI Health Records Copilot

This GenAI-powered agent helps users access and understand their health information by securely logging into healthcare portals, extracting records, and answering questions through ChatGPT.

---

## 🚀 Features
- Secure credential handling (Redis + Fernet)
- Human-in-the-loop challenge handler (MFA, CAPTCHA)
- AI-powered crawling, content extraction, summarization
- Consent tracking and full audit logs
- Test-friendly `test_portal` adapter for local dev

---

## 🔧 Setup

### 1. Clone and install dependencies
```bash
git clone https://github.com/stewmckendry/ai-delivery-sandbox.git
cd ai-delivery-sandbox
pip install -r requirements.txt
playwright install --with-deps
```

### 2. Setup environment
```bash
cp .env.sample .env
# Edit values: OPENAI_API_KEY, FERNET_KEY, etc.
```
To generate a Fernet key:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

## 🧪 Run a Full Test
```bash
python scripts/run_portal_test.py --portal test_portal --debug
```

Check logs in:
```
logs/portal_runs/<portal>_<timestamp>.json
data/audit_log.json
```

---

## 📁 Key Folders
- `app/` – core logic (orchestrator, adapter, crawler, etc.)
- `scripts/` – test runners, dev helpers
- `task_guides/` – Codex tasks + reviews
- `project/docs/` – design docs

---

## ✅ Status
Core functionality implemented. Ready for structured tests and real portal adapters.