## WP20 – Google Drive Storage Integration (v2)

### 🎯 Objective
Enable secure export of final artifacts and key files to Google Drive for downstream access, editing, and review. Replaces local storage used in WP18.

### 📦 Scope of Work
**In Scope:**
- OAuth integration (via service account)
- Drive folder routing by project, gate, artifact
- Upload + overwrite detection
- Replace `commitArtifact` logic from WP18 that stores artifact to disk as part of the 'assemble_artifact' toolchain - to be replaced by `storeToDrive`
- Add `storeToDrive` + `fetchFromDrive` tools (following the Tool class pattern like 'commitArtifact')
- Populate and persist Drive URL to `DocumentVersionLog`
- Support markdown and PDF format upload

**Out of Scope:**
- Google Docs real-time editing (UI layer)
- Review/approval workflows (covered elsewhere)

### 🔧 Enhancements to Original Scope
- File format detection and PDF export (optional)
- Sharing settings: default org visibility
- `drive_structure.yaml`: config for folder routing
- Support for GPT-safe document fetch from Drive (e.g., preview chunks)

### 🚀 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/tools/tool_wrappers/storeToDrive.py` | Uploads files to Drive under structured folder |
| `app/tools/tool_wrappers/fetchFromDrive.py` | Retrieves and previews files from Drive |
| `project/reference/drive_structure.yaml` | Metadata → folder path mapping |
| `project/test/WP20/test_drive_storage.py` | Toolchain tests |
| `project/test/WP20/test_results.md` | Logs of outcomes |
| `project/build/wps/WP20/WP20_implementation_notes.md` | Drive API, OAuth, structure design |
| `project/build/wps/WP20/gpt_user_flow_with_drive.md` | GPT user flow with Drive integration |

### ✅ WP20 Task List

#### 🎨 Design
- Define folder naming logic
- Identify metadata schema for Drive routing

#### 🔐 OAuth Setup
- Create and configure service account
- Setup credentials in secure config

#### 🛠️ Build Tools
- `storeToDrive.py`: upload logic + overwrite detection
- `fetchFromDrive.py`: retrieval and URL return

#### 🔧 Patch Integration
- Replace WP18 commit logic
- Log Drive URL to `DocumentVersionLog`

#### 🧪 Testing
- Upload test artifacts and validate fetch
- Handle errors (auth fail, quota, duplicates)

#### 📄 Docs + Review
- Write implementation spec and results
- Final review and handoff

### ✅ Acceptance Criteria
- [ ] Files upload to correct folders
- [ ] Overwrites handled gracefully
- [ ] File link returned and stored in DB
- [ ] Fetch returns URL or preview payload

### 🧱 Dependencies
- WP18 (artifact generation + commitArtifact logic)
- WP1a (GPT interface usage)

### 📥 Inputs
- Artifact metadata: gate_id, artifact_id, version
- Final output: markdown or PDF

### 📤 Outputs
- File uploaded to Drive
- URL returned to GPT or user

### 🧠 Notes
- Drive API v3 with Python SDK
- Credentials stored in environment config
- Folder structure: `/PolicyGPT/<project>/<gate>/<artifact>`

### 🔄 Next Steps
- Create and validate `storeToDrive` and `fetchFromDrive`
- Patch `assemble_artifact` to call Drive uploader
- Test file lifecycle: write, overwrite, fetch
- Document structure and auth setup

### 📚 References
- `commitArtifact.py`, `DocumentVersionLog`
- `WP18_exit_report.md`, `dense_artifact_generation.md`
- Google Drive Python SDK: https://developers.google.com/drive/api/guides
