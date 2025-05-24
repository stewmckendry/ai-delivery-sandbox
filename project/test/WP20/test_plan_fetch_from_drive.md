## WP20 Test Plan – fetchFromDrive Tool

### 🎯 Objective
Validate that `fetchFromDrive.py` correctly locates and returns the uploaded PDF from Google Drive using gate ID, artifact ID, and version.

### ⚙️ Setup Steps
1. Ensure `.env` contains:
   ```env
   GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON_PATH=.secrets/service_account.json
   ```
2. Confirm uploaded file exists:
   - Gate ID: `0`
   - Artifact ID: `investment_proposal_concept`
   - Version: `v0.1`
   - Filename: `investment_proposal_concept_vv0.1_20250524T165711.pdf`

### ▶️ Test Execution
Use a CLI runner or REPL:
```python
from app.tools.tool_wrappers.fetchFromDrive import Tool

output = Tool().run({
    "gate_id": "0",
    "artifact_id": "investment_proposal_concept",
    "version": "v0.1"
})
print(output)
```

### 📥 Expected Output
```json
{
  "file_name": "investment_proposal_concept_vv0.1_20250524T165711.pdf",
  "webViewLink": "https://drive.google.com/file/d/1oRm_K59DNp2Iqou1DVJutrCE_Aiu709S/view?usp=drivesdk"
}
```

### ✅ Success Criteria
- No error raised
- Filename returned matches expected pattern
- URL opens and matches uploaded file

---

📁 File uploaded May 24, 12:57 PM and appears in `gate_0/investment_proposal_concept/`