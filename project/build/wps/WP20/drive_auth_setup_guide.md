## Google Drive API Setup for PolicyGPT (WP20)

### 1. Enable Google Drive API
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create or select a project
- Navigate to **APIs & Services > Library**
- Search for **Google Drive API** and click **Enable**

### 2. Create a Service Account
- Go to **APIs & Services > Credentials**
- Click **Create Credentials > Service account**
- Give it a name like `policygpt-drive-uploader`
- After creation, go to the service account details
- Under **Keys**, click **Add Key > Create new key > JSON**
- Save the downloaded JSON in a secure local path (`./secrets/service_account.json`)

### 3. Share Drive Folder (Optional)
- Go to Google Drive
- Create a root folder named `PolicyGPT`
- Right-click and choose **Share**
- Add the **service account email** (e.g., `...@project.iam.gserviceaccount.com`) with **Editor** access

### 4. Add OAuth Config to Environment
- Copy sample config from `example_env_drive_oauth.yaml`
- Add to your `.env` file (for local)
- Add same vars to **Railway > Environment Variables** (for cloud)

### 5. Install SDK + Auth Packages
```bash
pip install google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib
```

### 6. Test Access
Run a local test script to:
- Load credentials from `.env`
- List or create a test file in the Drive root or `PolicyGPT` folder
- Confirm you get back a valid `webViewLink`

### 7. Security
- Never commit the JSON file
- Rotate keys periodically
- Limit scope to `https://www.googleapis.com/auth/drive.file`