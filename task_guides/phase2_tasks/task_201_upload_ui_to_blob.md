# Task 201: Upload UI to Azure Blob

## 🎯 Goal
Allow users to securely upload files (downloaded from health portals via Operator) to Azure Blob Storage using a user-friendly web interface.

## 📂 Content
This is part of Phase 2 - refer to phase2_operator_architecture.md for overall architecture.

## 📂 Target Files
- `app/api/upload.py` (new)
- `app/web/upload_form.html` (new)
- `app/storage/blob.py` (new or extend)

## 📋 Instructions
- Create a minimal HTML+JS page with drag-drop upload field
- Backend generates **SAS upload URL** (15 min TTL)
- When user completes Operator session, Copilot provides upload link
- Upon upload:
  - Store to Blob container (by user/session key)
  - Log metadata (portal, timestamp, filename)

## 🔐 Security Notes
- Use SAS token scoped to 1–5 files max
- Validate file type (PDF, HTML, TXT)
- Files should expire after 72 hours

## 🧪 Test
- Manual test: upload 2 files via browser
- Confirm blob visible in Azure dashboard
- Confirm metadata log

## ✅ What to Report Back
- Upload form URL
- Example blob URL post-upload
- Example metadata log entry

This is the secure bridge between user-controlled download and Copilot-driven ETL.