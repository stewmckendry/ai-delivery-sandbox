# Codex Agent Task: Raw File Store Service

## 🎯 Goal
Create a utility to save raw HTML and PDFs with metadata indexing.

## 📂 Target File
- `app/storage/files.py`

## 📋 Instructions
- Function: `save_file(content, filename, portal_name, metadata)`
- Store content in `data/raw/` as `<portal>_<timestamp>.<ext>`
- Update `data/raw/file_index.json` to log:
  - filename
  - portal name
  - timestamp
  - metadata dict
- Create folder + index file if not exists
- Accept `str` or `bytes` content

## ✅ What to Report Back
- File code
- Sample usage and resulting file paths
- Example `file_index.json` output
- Notes on how to test locally

Refer to `task_guides/review_checklist.md` for format.