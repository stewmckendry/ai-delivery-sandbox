## WP9 Deployment Steps

### 🧠 Context
WP9 introduced ingestion tools and DB logging for user input processing. Deployments must ensure the ingestion pipeline, memory system, and DB schema are aligned.

---

### ✅ Pre-Deployment Checklist
- [ ] Clone repo and activate virtual env
- [ ] Ensure access to `SQL Server` instance
- [ ] Set `DATABASE_URL` in `.env`

---

### 📦 DB Schema Setup
Run once to initialize tables:
```bash
python3 -c "from app.db.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

If needed, to reset:
```bash
python3 -c "from app.db.database import Base, engine; Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)"
```

---

### ⚙️ Tool Usage (CLI)
To test ingestion manually:
```bash
python3 -m app.tools.tool_wrappers.cli_ingest_runner logs/input_traces/samples/test_input_samples.txt --type uploadTextInput
```

Other types:
```bash
--type uploadFileInput
--type uploadLinkInput
```

---

### 🧪 Verification
Check YAML written:
```bash
ls logs/ingest_traces/
```

Check DB entries:
```sql
SELECT * FROM prompt_logs ORDER BY timestamp DESC;
```

---

### 📎 Notes
- Ensure `.env` points to correct SQL instance
- Use the latest `structure_input` format for tools

— ProductPod