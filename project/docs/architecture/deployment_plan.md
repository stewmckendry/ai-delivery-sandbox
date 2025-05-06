## 🚀 Deployment Architecture – CareerCoach MVP

### 1. ✅ API Hosting: Railway
- Hosts our FastAPI backend
- GitHub-connected, deploys on push
- Secrets managed via Railway UI
- Logs and metrics available for observability

#### 🛠 Connecting GitHub to Railway
- You must authorize Railway to access your GitHub account.
- If `ai-delivery-sandbox` doesn't appear:
  1. Go to [https://railway.app/dashboard](https://railway.app/dashboard)
  2. Click your profile icon → **Account Settings** → **GitHub Integration**
  3. Re-authorize GitHub and enable access to `ai-delivery-sandbox`

---

### 2. 📁 Static Reference Files
- Stored in GitHub (`project/inputs/`)
- Fetched via raw URLs
- Version-controlled and inspectable
- Future: deploy to CDN (Vercel or Cloudflare Pages)

---

### 3. 🔌 Airtable + Notion Integration

#### 🔐 Secrets
- Store tokens as Railway environment variables
  - `AIRTABLE_API_KEY`, `NOTION_API_TOKEN`
  - `AIRTABLE_BASE_ID`, `NOTION_DATABASE_ID`

#### ✅ Airtable Setup (for Beginners)
1. Go to [https://airtable.com](https://airtable.com) → Create a free account.
2. Start a **new base** → Name it `CareerReflections`
3. Add columns: `session_id`, `career_id`, `prompt_id`, `text`, `timestamp`
4. Go to **Account → Developer Hub** to create a Personal Access Token
5. Find your Base ID by opening your base in a browser. The URL will look like:
   ```
   https://airtable.com/appABC123XYZ/Table1
   ```
   Copy the part starting with `app...` — that's your `AIRTABLE_BASE_ID`

#### ✅ Notion Setup (for Beginners)
1. Go to [https://notion.so](https://notion.so) → Create a free account.
2. Create a new database (table) called `Journals`
3. Add properties: Career (title), Reflection (text), Prompt (text), Created Time (date)
4. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
5. Click **New Integration**
   - Name it (e.g., `careercoach-dev`)
   - Important: Make sure you create it while you're logged into the **same workspace** as your Journals database
   - Enable **Read content** and **Insert content** permissions
6. Copy the generated Notion API token
7. Return to your `Journals` database
8. Click the **••• (three-dot menu)** in the top-right corner
9. Click **Connections** → Search for your integration by name (e.g., `careercoach-dev`) and connect it
10. To get the `NOTION_DATABASE_ID`, open your database in a full-page view. The URL will look like:
   ```
   https://www.notion.so/1eb0cdbf497780f8828fd91546ed73c9?v=1eb0cdbf497780d6ae55000cd24e76c7
   ```
   The first 32-character string before `?v=` is your database ID: `1eb0cdbf497780f8828fd91546ed73c9`

---

### 4. 🧠 Custom GPT Integration

#### 🔍 Discoverability
- Publish GPT with a public profile (e.g., "CareerCoach-GPT")
- Add rich description, emoji tags, example prompts
- Share direct link in blog, docs, and product homepage

#### 👥 Multi-user Support
- Memory is OFF in GPT (stateless)
- Each session handled via backend tools with session_id
- No risk of cross-user leakage
- Can support many concurrent users

---

### 5. 🔁 CI/CD via GitHub Actions

#### Triggers:
- `sandbox-*` push → test + lint
- `main` merge → deploy to Railway (default)
- **You can override this by setting Railway's deploy branch to `sandbox-silent-otter` in project settings**

#### Artifacts:
- `.env.template` for local dev
- `deployment_plan.md` as runbook

---

### 📦 Local Development Setup

To run the FastAPI backend locally, follow these steps:

#### 1. 📁 Clone the Repo
```bash
git clone https://github.com/stewmckendry/ai-delivery-sandbox.git
cd ai-delivery-sandbox
```

#### 2. 🛠 Set Up Your Environment Variables
Copy the template file and fill in secrets:
```bash
cp .env.template .env
```
Update `.env` with your Airtable and Notion API tokens and IDs.

#### 3. ▶️ Run the App Locally
You’ll need Python 3.9+ and `pip`:
```bash
pip install -r requirements.txt
uvicorn project.app.main:app --reload
```
This will start the FastAPI app at `http://127.0.0.1:8000`

#### 4. 🧪 Test the API Endpoints
You can test endpoints with `curl`, `httpie`, or `Postman`. Example:
```bash
curl "http://127.0.0.1:8000/load_prompt?prompt_id=p1"
```
Or use the built-in Swagger docs at:
```
http://127.0.0.1:8000/docs
```

Note: You must manually create sample prompts under `project/inputs/prompts` as JSON files (e.g., `p1.json`) to test prompt loading.

---

### 🚀 Deploy to Railway (Production or Sandbox)

1. Go to [https://railway.app](https://railway.app) and create a new project.
2. Connect it to the GitHub repo. If `ai-delivery-sandbox` is missing, see Step 1 above.
3. Add environment variables in Railway UI:
   - `AIRTABLE_API_KEY`
   - `AIRTABLE_BASE_ID`
   - `NOTION_API_TOKEN`
   - `NOTION_DATABASE_ID`
4. Set the deploy branch:
   - Go to your Railway project
   - Click **Settings** in the sidebar (gear icon)
   - Under **GitHub** settings, find the **Branch** dropdown
   - Change from `main` to `sandbox-silent-otter`
   - Click **Save** if prompted
5. Set the start command in the Railway **Deploy** tab:
   ```bash
   uvicorn project.app.main:app --host 0.0.0.0 --port 8000
   ```
6. Push to the selected branch to deploy.
7. Confirm deployment at:
```
https://ai-careercoach-production.up.railway.app/docs
```
(Or the sandbox subdomain if configured)

---

Ready to ship 🚀