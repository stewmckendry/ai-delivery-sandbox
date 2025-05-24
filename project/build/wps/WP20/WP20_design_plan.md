## WP20 Design Plan – Google Drive Integration

### Repo + Branch
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Token:** _[stored in memory for future access]_  

---

## 🧩 Goals & Scope
Enable secure, structured upload and retrieval of final artifacts via Google Drive using OAuth and Python SDK.

### Key Deliverables
| File | Purpose |
|------|---------|
| `storeToDrive.py` | Uploads markdown/PDFs into `/PolicyGPT/<project>/<gate>/<artifact>` folder paths |
| `fetchFromDrive.py` | Fetches preview or full file from Drive based on metadata |
| `drive_structure.yaml` | Config for folder routing logic |
| `test_drive_storage.py` | CLI test for upload + fetch tool |
| `test_results.md` | Record of test output |
| `WP20_implementation_notes.md` | Design + technical integration notes |
| `gpt_user_flow_with_drive.md` | GPT scenario using Drive links |

---

## 📋 Task Breakdown

### Design Phase
- [x] Read WP20 scope and upstream toolchains
- [x] Review user journeys, gate schema, and architecture
- [ ] Define folder routing logic (drive_structure.yaml)
- [ ] Confirm metadata inputs needed from artifact (gate_id, artifact_id, version)

### OAuth + API
- [ ] Configure service account and secure credentials (local via .env, cloud via Railway env vars)
- [ ] Validate SDK authentication (token refresh, scope)

### Tool Development
- [ ] Build `storeToDrive.py` with overwrite detection + upload logic
- [ ] Build `fetchFromDrive.py` with preview / full fetch based on format
- [ ] Validate integration with `assemble_artifact_chain.py`

### Logging + Patching
- [ ] Patch `assemble_artifact_chain` to call `storeToDrive`
- [ ] Update `DocumentVersionLog` with final Drive URL

### Testing
- [ ] Write test harness: `test_drive_storage.py`
- [ ] Log results to `test_results.md`
- [ ] Simulate errors (auth fail, quota, invalid path)

### Docs + Review
- [ ] Author `implementation_notes.md` with setup details
- [ ] Draft user flow in `gpt_user_flow_with_drive.md`

---

## 🧠 Technical Design

### Google Drive Connector
- Uses Python SDK with service account auth
- Reads folder config from `drive_structure.yaml`
- Uploads files with version tag in filename
- Captures and returns webViewLink URL

### Metadata Design
#### Stored in DB (`DocumentVersionLog`)
- `doc_version_id`, `gate`, `artifact_name`, `file_path`, `google_doc_url`, `submitted_by`, `submitted_at`

#### Embedded in Drive file (via description or folder)
- Artifact ID, Gate ID, Version, Timestamp
- Origin: PolicyGPT

---

## 🧠 E2E Integration Pathways

### Journey A – Iterative Drafting
- GPT composes section → validator passes → `assemble_artifact_chain.py`
- On commit, `storeToDrive.py` uploads final doc
- `google_doc_url` saved to `DocumentVersionLog`
- User receives link for review or export

### Journey B – Fast Track / External Edit
- Full doc uploaded by user → PolicyGPT reads and validates
- User initiates commit to Drive
- Drive URL returned and stored

### Journey C – Feedback Loop
- Reviewer uploads changes to same Drive folder
- PolicyGPT reads updated file, diffs with prior
- New version committed if accepted

---

## ❓Open Questions + Inputs Confirmed
- ✅ Overwrite = timestamp suffix
- ✅ OAuth via .env (local) + Railway env vars (cloud)
- ✅ Artifacts always markdown or PDF
- ✅ One upload per artifact
- ✅ Drive URLs are persistent per version
- ⏳ tool_catalog.yaml still missing (404)

---

## 🚧 Risks + Mitigations
- **OAuth misconfiguration blocks file access**  
  _Mitigation_: Use env-var-based credentials + local `.env` fallback; validate at init with test token exchange

- **API quota/limits could impact large runs**  
  _Mitigation_: Implement exponential backoff and log quota status; allow manual retry in CLI and future UI

- **Folder naming collisions if schema not enforced**  
  _Mitigation_: Use structured folder paths and filename timestamps; add uniqueness validators before upload

---

## ⏭️ Next Steps
- Commit this plan + task list
- Begin OAuth and routing logic setup
- Build Drive connector tools (store/fetch)
- Patch toolchain and run integration tests
- Finalize documentation and test outputs for review