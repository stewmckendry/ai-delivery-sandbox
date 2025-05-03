## 🚀 Deployment Architecture – CareerCoach MVP

### 1. ✅ API Hosting: Railway
- Hosts our FastAPI backend
- GitHub-connected, deploys on push
- Secrets managed via Railway UI
- Logs and metrics available for observability

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
- No user auth or PII — all sessions anonymized

#### ✅ Airtable Setup
- One table: `CareerReflections`
- Columns: session_id, career_id, prompt_id, text, timestamp

#### ✅ Notion Setup
- One database: `Journals`
- Properties: Career, Reflection, Prompt, Created Time
- Used for narrative journaling + teacher summaries

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
- `main` merge → deploy to Railway
- Manual → tool schema upload to Custom GPT

#### Artifacts:
- `.env.template` for local dev
- `deployment_plan.md` as runbook

---

Ready to ship 🚀