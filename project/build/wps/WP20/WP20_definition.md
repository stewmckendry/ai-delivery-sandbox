## WP20 – Google Drive Storage Integration

### 🎯 Objective
Build tools and workflow to export final drafts and key session files to a structured Google Drive folder system. This allows downstream users to access and collaborate on generated outputs.
- This work builds on `WP18`, which assemble drafted sections into complete artifacts.  It has a placeholder toolchain step for storage called `commitArtifact`.


### 📦 Scope of Work
**In Scope:**
- OAuth integration to Google Drive (via service account)
- Folder structure by project, gate, and artifact
- Upload and overwrite detection
- `storeToDrive` and `fetchFromDrive` tool implementations
- Store and maintain URLs in `google_doc_url`.
- Section-level export
- Version tracking in `DocumentVersionLog`


**Out of Scope:**
- Google Docs real-time editing (future UI enhancement)
- Approval routing and e-signature (handled by other systems)

### 🚀 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/tools/tool_wrappers/storeToDrive.py` | Uploads document to Google Drive under correct folder |
| `app/tools/tool_wrappers/fetchFromDrive.py` | Downloads files from Drive for GPT review |
| `project/config/drive_structure.yaml` | Defines folder templates and naming conventions |

### ✅ Acceptance Criteria
- [ ] Authenticated upload and fetch to/from Drive works with tokens
- [ ] Files routed to correct project > gate > artifact folders
- [ ] Can support preview and fetch for editing or referencing
- [ ] Supports markdown, PDF, and YAML formats

### 🔗 Dependencies
- WP18 (assembled artifacts to upload)
- WP1a (feedback and review tools)

**Links:**
- Design: `dense_artifact_generation.md`

### 📥 Inputs
- Final document YAML or markdown
- metadata (project_id, gate_id, artifact_id)

### 📤 Outputs
- File uploaded to Google Drive
- URL returned for reference

### 🧠 Notes
- Must ensure file overwrite detection to avoid duplicates
- Use Google Drive API + Python SDK with service account auth