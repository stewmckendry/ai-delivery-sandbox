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

Generate a short-lived API token:
```bash
python scripts/create_token.py --user <id> --agent gpt --portal <portal> --minutes 60
```
The token is signed using the `DELEGATION_SECRET` in your `.env` file and expires
after the number of minutes you provide. When it expires, generate a new token
and update the GPT configuration.

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

## 🗑️ Data Retention
- Challenge screenshots saved under `/tmp` are deleted after a response is received.
- Files written to `data/raw/` can be removed once processed by setting `RAW_CLEANUP=1`.

---

## 🚀 Deployment
See [`project/docs/railway_deployment_guide.md`](project/docs/railway_deployment_guide.md) for instructions to deploy the FastAPI backend and web client on Railway.
For running the Chroma vector database separately, see [`project/docs/chroma_deployment_guide.md`](project/docs/chroma_deployment_guide.md).

---

## ✅ Status
Core functionality implemented. Ready for structured tests and real portal adapters.