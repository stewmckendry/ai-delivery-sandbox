# 🛠️ Deployment Guide – Concussion Recovery GPT Tools

This guide explains how to run, configure, deploy, and validate the full stack for the concussion recovery GPT system.

---

## 🔁 System Overview

```
[Custom GPT]
   |
   | ↔️ API Calls (triage, symptom logging, export)
   ↓
[FastAPI Server (Railway-hosted)]
   ↔️ YAML reference files (GitHub)
   ↔️ Azure SQL (tracker + symptom exports)
   ↔️ Azure Blob (PDF + FHIR output)
   ↓
[Power BI Dashboard] ← SQL views
```

---

## 🧱 Core Components

- **Custom GPT**: Presents prompts using OpenAPI schema and `x-gpt-action`
- **FastAPI App** (`main.py`): Hosts tool routes for triage, symptom logging, stage inference, export
- **OpenAPI** (`openapi.json`): Defines all tool endpoints for GPT use
- **Azure SQL**: Stores structured logs for analysis
- **Azure Blob Storage**: Persists PDF/FHIR outputs
- **Power BI**: Connects to SQL for dashboard views

---

## ⚙️ Local Setup

### 1. Clone Repo
```bash
git clone https://github.com/stewmckendry/ai-delivery-sandbox.git
cd ai-delivery-sandbox
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file:
```ini
AZURE_SQL_CONNECTION_STRING=your-azure-sql-conn-string
AZURE_STORAGE_CONNECTION_STRING=your-blob-storage-conn-string
BLOB_CONTAINER_NAME=concussion-exports
```

### 4. Run Server
```bash
uvicorn app.main:app --reload
```
Then visit `http://localhost:8000/docs` for Swagger UI.

---

## ☁️ Railway Deployment

### 1. Create Railway Project
- Visit [https://railway.app](https://railway.app)
- Click "New Project" → "Deploy from GitHub repo"
- Select the `ai-delivery-sandbox` repository
- Choose the `sandbox-silver-tiger` branch

### 2. Configure Environment Variables
Under the Railway project:
- Click on the ⚙️ Settings tab → Environment Variables
- Add:
  - `AZURE_SQL_CONNECTION_STRING`
  - `AZURE_STORAGE_CONNECTION_STRING`
  - `BLOB_CONTAINER_NAME`

### 3. Define Service
- Railway should auto-detect `uvicorn app.main:app`
- If not, define the entry manually in the Deploy tab

### 4. Trigger a Build
- Push changes to GitHub or click “Deploy” to trigger a manual build
- Monitor logs under Deploy → Logs tab

### 5. Verify Deployment
- Visit `https://<project>.up.railway.app/docs`
- This opens **Swagger**, a built-in interactive UI for testing your endpoints.
- No setup needed—it's bundled with FastAPI!

---

## 🧪 Test Tools

### 1. Swagger Interface Setup
- Swagger is automatically served at `/docs`
- Navigate to your deployed Railway app:
```
https://<your-app>.up.railway.app/docs
```
- Use the interactive forms to test each endpoint without any custom client.

### 2. Custom GPT Configuration
- Set OpenAPI URL to:
```text
https://<your-project>.up.railway.app/openapi.json
```
- GPT will load the schema and use `x-gpt-action` instructions

### 3. Test Export to SQL
- Log data using `/log_symptoms` or `/log_incident_detail`
- Trigger export with `/export_to_sql`
- Open Azure SQL and confirm rows exist in:
  - `symptom_log_export`
  - `tracker_export`

### 4. Test Blob Storage Output
- Use `/export_summary` with a valid `user_id`
- Confirm Blob creation in your Azure container
  - You can check this via Azure Portal → Storage Accounts → Your Container → Files

---

## ☁️ Azure Database Setup

### 1. Create Azure SQL Database
- Go to [portal.azure.com](https://portal.azure.com)
- Click "Create a resource" → "SQL Database"
- Select:
  - Resource group
  - Database name (e.g., `concussionDB`)
  - Server (create new or use existing)
- Choose "Basic" pricing tier for demo/testing

### 2. Configure SQL Server Access
- Allow Azure services and your IP to access server
- Add firewall rules under "Set server firewall"
- Note the server name, username, and password for connection string

### 3. Run Initial Schema
- Use `app/db/db_models.py` to create tables (if using SQLAlchemy migrations)
- Or run SQL DDL scripts manually in Azure Data Studio:
```sql
CREATE TABLE tracker_export (...);
CREATE TABLE symptom_log_export (...);
```

### 4. Confirm Connection
- Use any SQL client (Azure Data Studio, DBeaver)
- Input the connection string and validate access

---

## 📊 Power BI Dashboard

### 1. Confirm Azure SQL Connection
- Open Power BI Desktop
- Choose “Azure” → “Azure SQL Database”
- Enter server name (e.g., `my-server.database.windows.net`) and DB name
- Authenticate using SQL login

### 2. Import Data Tables
- Select:
  - `symptom_log_export`
  - `tracker_export`
- Load into model view

### 3. Build Views
- Suggested visualizations:
  - Symptom count trends over time
  - Red flag frequency by age/sport
  - Recovery stage progression

### 4. Configure Auto-Refresh
- Publish to Power BI Service
- Go to Dataset Settings → Schedule Refresh
- Set refresh frequency (e.g., daily)
- Use Data Gateway if needed for external SQL

---

## ✅ Completion Checklist

- [x] FastAPI boots locally and on Railway
- [x] Swagger accessible at `/docs`
- [x] GPT can call routes via OpenAPI
- [x] Azure SQL logs new triage + symptom data
- [x] PDF/FHIR files saved to Blob and linked
- [x] Dashboard views appear in Power BI