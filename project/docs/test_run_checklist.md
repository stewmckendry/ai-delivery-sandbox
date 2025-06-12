# ✅ ETL Test Run Checklist

Use this checklist to run and evaluate a full ETL pipeline test for a given portal.

---

## 🔧 Setup
- [ ] Installed all dependencies
- [ ] `.env` configured with:
  - [ ] `OPENAI_API_KEY`
  - [ ] `FERNET_KEY`
  - [ ] `USE_FAKE_REDIS=1` (optional for local only)

---

## ▶️ Run Command
```bash
python scripts/run_portal_test.py --portal test_portal --depth 2 --debug
```

---

## 📋 Outputs to Review
- [ ] `data/audit_log.json` – Consent + action logs
- [ ] `logs/portal_runs/` – Run summary JSON
- [ ] Extracted content types (e.g., `lab_result`, `visit_note`)
- [ ] Cleaned + summarized output chunks
- [ ] Any challenge screenshots (if simulated)

---

## 🛠️ Bugs or Enhancements
For each of the following, check:
- [ ] Content missed during scrape?
- [ ] Pages not traversed?
- [ ] Chunking/summarization incorrect?
- [ ] Deduplication failure?
- [ ] Wrong type tagging (e.g., lab misclassified)?

Log issues as new Codex tasks with `test_run` tag and attach log file if needed.

---

## 🔁 Repeat for:
- [ ] Public real site (no login)
- [ ] Auth-required portal (simple login)
- [ ] Portal with CAPTCHA or MFA

---

# 📦 To Add More Test Portals
1. Copy `app/adapters/test_portal.py` → `app/adapters/test_portal_2.py`
2. Modify page structure, HTML, and PDF contents
3. Update `.env` with new portal’s credentials
4. Run: `--portal test_portal_2`

---

# 🌐 To Run Against Real Portal
- Implement scraper in `app/adapters/real_portal_name.py`
- Add login logic and challenge handler
- Update `.env` with real credentials
- Run:
```bash
python scripts/run_portal_test.py --portal real_portal_name
```

✅ This framework supports progressive, repeatable ETL validation across all types of portals.