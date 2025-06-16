# Task 206: Azure Blob Retention and Cleanup

## 🎯 Goal
Prevent unbounded storage growth and ensure uploaded files are purged after processing or a defined TTL (time to live).

## 📂 Target Files
- `app/storage/blob.py`
- `scripts/cleanup_blobs.py` (new)

## 📋 Instructions
- Enable TTL cleanup:
  - Option 1: Azure lifecycle policy (external setup)
  - Option 2: Script to list + delete blobs older than N hours
- Add a helper in `blob.py` to fetch blob metadata + age
- CLI script to delete expired blobs (run via cron or CI)
- Optional: delete files after successful ETL ingestion

## 🧪 Test
- Upload mock files with timestamps >24hrs
- Run script with threshold = 1h
- Confirm old blobs deleted, recent ones remain

## ✅ What to Report Back
- TTL threshold used
- Number of blobs deleted in dry-run + actual
- Risk notes (e.g., shared prefix issues)

This task ensures compliance and keeps storage cost under control.