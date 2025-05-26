# ✅ WP7 Test Plan: Project Profile Engine Integration

## 🎯 Objectives
- Verify IngestInputChain successfully triggers input upload and project profile generation.
- Confirm `project_id` flows into DB via memory_sync from GenerateSectionChain.
- Confirm project metadata is saved and reflected in DocumentVersionLog via AssembleArtifactChain.

## ⚙️ Setup Steps
1. Ensure DB schema includes `project_id` fields and foreign keys (run the final SQL migration).
2. Set environment variable: `OPENAI_API_KEY`.
3. Place test file `test_upload.txt` in root directory with content:
   ```
   Project Pegasus is sponsored by the Ministry of Transport. Estimated budget is $100M...
   ```

## 🧪 Test Steps
### 1. Ingest File Input
- **Input:**
  ```json
  {
    "input_method": "file",
    "file_path": "test_upload.txt",
    "metadata": {
      "artifact_id": "pegasus_charter",
      "gate_id": 1,
      "user_id": "test_user",
      "session_id": "s1"
    }
  }
  ```
- **Expected Output:**
  - status: `profile_saved`
  - non-null `project_id`
  - project profile dict with extracted values

### 2. Generate Section
- **Input:**
  ```json
  {
    "artifact": "pegasus_charter",
    "section": "problem_statement",
    "gate_id": "1",
    "user_id": "test_user",
    "session_id": "s2",
    "project_id": "pegasus"
  }
  ```
- **Expected Output:**
  - DB row in `artifact_section` and `reasoning_trace` with `project_id = 'pegasus'`

### 3. Assemble Artifact
- **Input:**
  ```json
  {
    "artifact_id": "pegasus_charter",
    "gate_id": "1",
    "version": "v1",
    "project_id": "pegasus"
  }
  ```
- **Expected Output:**
  - DB row in `document_version_log` with `project_id = 'pegasus'`

## 📦 Cleanup
- Manually clear test rows from `project_profile`, `artifact_section`, `reasoning_trace`, `document_version_log`.