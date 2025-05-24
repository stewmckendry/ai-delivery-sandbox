## Google API Client + OAuth Library Primer for WP20

### 🔌 Libraries We Use

#### `googleapiclient.discovery.build`
- Builds a service object for the specified API and version.
- We use: `build("drive", "v3", credentials=creds)` → creates Google Drive client.

#### `googleapiclient.http.MediaInMemoryUpload`
- Wraps content (like markdown string) in memory as a file.
- Required by the Drive API to simulate file upload.
- We use: `MediaInMemoryUpload(data, mimetype="text/markdown")`

#### `google.oauth2.service_account`
- Loads service account credentials from JSON.
- We use: `Credentials.from_service_account_file(json_path, scopes=...)`
- Returns an object that is compatible with all Google client APIs.

### 🛠️ How We Use It

1. Load env var path to service account JSON
```python
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON_PATH")
```

2. Authenticate
```python
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
```

3. Connect to Drive
```python
service = build("drive", "v3", credentials=creds)
```

4. Upload file
```python
media = MediaInMemoryUpload(file_data.encode("utf-8"), mimetype="text/markdown")
file = service.files().create(body=file_metadata, media_body=media).execute()
```

5. Get output
```python
file["webViewLink"]  # Public or shared URL
```

### 📦 What's Happening Under the Hood
- OAuth handles JWT auth from service account to Google Drive.
- `build(...)` generates endpoint bindings using API discovery.
- Files and folders are represented by metadata (dict) in Drive.
- Folders are just files with `mimeType="application/vnd.google-apps.folder"`.
- Parents are passed by ID (not path strings).

For more: https://developers.google.com/drive/api/guides/upload-files