## Multi-User, Multi-Project Design for Google Drive Integration

### 🎯 Objective
Ensure that uploads from different users and projects remain isolated and traceable in Drive.

### 📁 Drive Folder Strategy
Root folder: `PolicyGPT`

Subfolders:
- `/PolicyGPT/<project_id>/<gate_id>/<artifact_id>/`
- Example: `/PolicyGPT/housing-grants/gate4/affordability-model/`

### 🔐 Access Model
- **Service account** acts on behalf of the system.
- Drive folder shared with contributors for external access if needed.
- Folder-level sharing supported (optional).

### 🧠 Metadata Routing
- `project_id` must be added to tool input + schema
- `drive_structure.yaml` already updated to anticipate this
- `storeToDrive.py` and `_get_or_create_folder_structure` will be extended when schema adds project_id

### ⚙️ Compatibility
- Each file is named with timestamp suffix to prevent overwrite
- Folder path includes key artifact metadata
- Future DB schema will link Drive URL to version, artifact, gate, and project

### 🧩 Risks
- If project_id is missing, uploads may collide under shared gate/artifact folders

### 🚧 Future Action (Logged)
- Add `project_id` to DB, schemas, and tool inputs (tracked in WP20 exit report)

This structure supports scaling across teams, gates, and multiple PolicyGPT deployments.