## WP20 Test Plan: Google Drive Upload Tool (`storeToDrive.py`)

### 🎯 Objective
Validate the `storeToDrive` tool by simulating a commit of an artifact to a Google Drive folder using mock artifact metadata and markdown.

### 🧪 Test Coverage
- OAuth service account config is loaded
- Folder structure is created under `/PolicyGPT/<gate>/<artifact>`
- Markdown file is uploaded and URL returned
- Web link is a valid Google Drive URL
- Handles error scenarios: auth failure, invalid parent ID, quota

---

### 🧰 Setup Steps

#### 1. Set Environment Vars (local `.env`)
```
GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON_PATH=.secrets/service_account.json
GOOGLE_DRIVE_SCOPES=https://www.googleapis.com/auth/drive.file
```

#### 2. Validate Service Account Access
Share the Drive `PolicyGPT` folder with the service account email (Editor access).

#### 3. Prepare Dummy Artifact Inputs
```sql
-- Optional SQL to insert mock artifact metadata (if DB validation needed)
INSERT INTO ArtifactSection (section_id, artifact_id, gate, content) VALUES
  ('sec-test-1', 'artifact-test', 'gate1', '## Section 1\nSome content here.');
```

---

### ▶️ Test Steps
Run from CLI: `python project/test/WP20/test_runner_store_to_drive.py`

Each test case will:
- Generate synthetic markdown
- Call the tool with mock artifact metadata
- Print or log the returned Google Drive link

---

### ✅ Expected Outputs
- Print output with valid Drive `webViewLink`
- No exceptions or tracebacks
- File appears in correct folder (manually verify in Drive)

---

### 🚨 Error Handling Tests
- Missing OAuth config → expected: traceback or error message
- Invalid parent folder ID → expected: Drive API returns error
- Rate limit exceeded → simulate with multiple runs

---

### 📦 Files
- `project/test/WP20/test_runner_store_to_drive.py` — executes test case