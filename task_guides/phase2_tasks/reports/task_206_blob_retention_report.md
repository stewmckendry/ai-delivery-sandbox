# ✅ Task 206 Report: Azure Blob Retention and Cleanup

## 📄 Summary
Implements retention controls for uploaded blobs using a CLI-based cleanup script. Expired blobs are deleted based on a TTL threshold.

## 🔧 Implementation
- `list_blob_info()` in `blob.py` returns blob metadata + age (in hours)
- `scripts/cleanup_blobs.py` removes blobs older than `--ttl-hours` threshold
- Includes `--dry-run` mode to preview deletions safely

## 🧪 Testing
- ✅ `pytest tests/test_cleanup_blobs.py -q`
- Mocks 2 blobs, only the expired one is deleted
- Logs output and verifies correct file was purged

## ✅ Files Changed
- `app/storage/blob.py` (+ metadata age logic)
- `scripts/cleanup_blobs.py` (new CLI tool)
- `tests/test_cleanup_blobs.py` (unit test)

## 🏁 Outcome
Storage now has automatic cleanup capabilities. Can be triggered via cron or CI to prevent unbounded growth.