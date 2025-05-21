### 🚀 WP3b Deployment Guide — Tool Registry API on Railway

This guide sets up the FastAPI-based Tool Registry service on Railway cloud.

---

### 🧱 Project Structure
- **App Entrypoint:** `main.py`
- **API Router:** `app/engines/api_router.py`
- **Tool Registry Core:** `app/tools/tool_registry.py`
- **Tool Catalog + Manifest:** `project/reference/tool_catalog.yaml`, `gpt_tools_manifest.json`

---

### 🪜 Deployment Steps (Railway)

#### 1. **Install Railway CLI (if not installed)**
```bash
npm install -g railway
```

#### 2. **Login and Create Project**
```bash
railway login
railway init
```

#### 3. **Set Entrypoint**
Ensure your `main.py` is the root of your FastAPI app. If needed, wrap with:
```python
# main.py
import uvicorn
from fastapi import FastAPI
from app.engines.api_router import router

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

#### 4. **Deploy to Railway**
```bash
railway up
```

---

### 🧪 Post-Deploy Checks
- `GET /status` → `{"status": "ok"}`
- `GET /tools` → List of all 18 tools
- `POST /tools/{tool_id}` → Should enforce schema validation

---

### 📦 Environment Notes
- The deployed version defaults to `source="github"` to load schemas from the latest tool catalog in GitHub

---

### 🔁 Future Extensions
- Add support for `RAILWAY_ENVIRONMENT` variable to auto-switch source loader
- Add auth, rate limiting, or telemetry as needed in WP3c