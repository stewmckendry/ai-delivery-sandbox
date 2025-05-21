### 🚀 WP3b Deployment Guide — Tool Registry API on Railway

This guide sets up the FastAPI-based Tool Registry service using the Railway deployment platform.

---

### 🧱 Project Structure
- **Entrypoint:** `main.py`
- **API Router:** `app/engines/api_router.py`
- **Tool Registry Logic:** `app/tools/tool_registry.py`
- **Schemas + Manifest:** `project/reference/tool_catalog.yaml`, `gpt_tools_manifest.json`
- **Dependencies:** `requirements.txt`

---

### 🛠 Railway Deployment (Standard Workflow)

#### 1. **Push Repo to GitHub**
Make sure the repo is available under your GitHub account.

#### 2. **Go to [Railway](https://railway.app)**
Click "New Project" → "Deploy from GitHub Repo" → Choose your `ai-delivery-sandbox` repo.

#### 3. **Configure Environment**
- **Root directory:** Use project root (where `main.py` lives)
- **Install command:**
```bash
pip install -r requirements.txt
```
- **Start command:**
```bash
python main.py
```

#### 4. **Set Port**
Ensure Railway is listening on port `8000`

#### ✅ Deployment URL
Once deployed, access the API at:
```
https://robust-adventure-production.up.railway.app
```

---

### ✅ Post-Deploy Verification
- `GET /status` → `{ "status": "ok" }`
- `GET /tools` → returns tool manifest
- `POST /tools/{tool_id}` → tool validation working

---

### 🔁 Extensions / Handoff
- Add `RAILWAY_ENVIRONMENT` or `DEPLOY_ENV` to toggle Git vs local loader
- WP3c may extend this with telemetry, secrets, or security wrappers

---