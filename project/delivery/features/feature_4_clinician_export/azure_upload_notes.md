## ☁️ Azure Blob Upload Notes

This document explains how we integrated Azure Blob Storage into the `export_summary` tool to deliver downloadable PDF summaries.

---

### 📦 What We Used
- **Storage Account**: `concussionexports`
- **Container**: `exports` (private access)
- **Method**: `upload_to_storage()` in `export_summary.py`
- **Security**: Generated **SAS token URLs** for temporary access

---

### 🛠 Setup Steps (completed)
1. Created Azure storage account and private blob container
2. Retrieved the **connection string** and **access key** from Azure Portal
3. Installed `azure-storage-blob` Python SDK

---

### 🧪 Upload Process
Inside `upload_to_storage()`:
- Connects using `BlobServiceClient.from_connection_string(...)`
- Creates a unique blob name using UUID
- Uploads the file with `blob_client.upload_blob`
- Generates a 1-hour signed SAS URL using `generate_blob_sas(...)`
- Returns a secure, user-specific PDF link

---

### 🔐 Why SAS URL?
- Container is private (no public reads)
- SAS allows time-limited, secure access per file
- Aligns with healthcare data sensitivity and export control

---

### ✅ Next Steps
- Rotate access keys periodically via Azure Portal
- In production, store credentials securely via environment variables
- Consider expiring files after fixed retention (e.g., 7 days)

---

The uploaded PDF links are now shareable via GPT or frontend apps, while keeping storage secure and auditable.