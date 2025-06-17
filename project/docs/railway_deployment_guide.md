# Railway Deployment Guide

## 🌟 Goal
Step-by-step instructions to deploy the FastAPI backend and upload web client on Railway.

---

## 📚 Required Files
- `Dockerfile`
- `requirements.txt`
- `.env` (local only; values entered into Railway dashboard)
- `Procfile` (optional if using Docker)

Ensure these files are committed in your GitHub repo before linking to Railway.

---

## 🔧 Environment Variables
Add the following in Railway's **Variables** tab:
```env
OPENAI_API_KEY=sk-...
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=...
DATABASE_URL=sqlite:///health_data.db
SECRET_KEY=supersecret
```

---

## 📝 Dockerfile
```Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y curl gnupg2 apt-transport-https build-essential \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/12/prod.list \
        > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🕹️ Local Test
Before deploying run:
```bash
uvicorn app.main:app --reload
```
Open `http://localhost:8000/docs` for API docs and `http://localhost:8000/upload` for the web form.

---

## 👩‍💻 Railway Setup Steps
1. Create a new Railway project and link your GitHub repo.
2. Add the environment variables above.
3. Ensure the Dockerfile is present. Railway will build and run it automatically.
4. Trigger a deploy.
5. Visit the deployed URL and verify:
   - `/upload` shows the upload form.
   - `/docs` loads the Swagger API docs.
   - APIs like `/ask` and `/summary` return expected data.
6. Check logs to confirm blob uploads and ETL flow.

Deployment is complete when the hosted URL serves the endpoints without errors.

