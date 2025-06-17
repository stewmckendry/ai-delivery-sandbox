# 🚀 Task 301: Railway Deployment Plan

## 🎯 Goal
Prepare an instruction guide for Stewart to deploy the FastAPI backend and upload web client to Railway.

Codex Agent should write a self-contained deployment guide Stewart can execute. This includes commands, required files, environment variable setup, and tests.

---

## 🧱 App Components to Deploy
1. **FastAPI App:**
   - `app/main.py`
   - APIs: `app/api/upload.py`, `app/api/etl.py`, `app/api/rag.py`, `app/api/status.py`

2. **Upload Web Client:**
   - `app/web/upload_form.html`

---

## 🔧 Environment Variables
Add these to Railway’s project environment settings:
```env
OPENAI_API_KEY=sk-...
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=...
AZURE_SQL_URL=sqlite:///health_data.db  # Or your actual DB URL
SECRET_KEY=supersecret  # Used for FastAPI sessions or auth if needed
```

---

## 🗂️ Required Files
- `Dockerfile`
- `requirements.txt`
- `Procfile` (optional if Docker used)
- `.env` (local only; values go into Railway’s dashboard)

---

## 📦 Dockerfile
```Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📜 requirements.txt (excerpt)
```
fastapi
uvicorn
httpx
python-dotenv
sqlalchemy
jinja2
azure-storage-blob
openai
```

---

## 🧪 Manual Test Commands
Run locally before deploying:
```bash
uvicorn app.main:app --reload
```
Then open:
- `http://localhost:8000/docs` (API docs)
- `http://localhost:8000/upload` (web form)

---

## 🚀 Railway Setup Steps
1. Create new Railway project
2. Add GitHub repo & link to this branch
3. Add environment variables from above
4. Add Dockerfile if not present
5. Deploy
6. Visit deployed URL to verify `/upload`, `/ask`, and `/summary`

---

## ✅ Done When
- Railway app URL serves `/upload` and `/docs`
- FastAPI APIs return expected data
- Logs confirm blob upload and ETL flow