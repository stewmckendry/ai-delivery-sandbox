# 📌 Deployment Addendum – Azure DBs + Admin Tools

This guide complements the main deploy guide with deeper coverage of Azure databases, storage tools, admin workflows, and schema setup.

---

## 🗂️ Overview: Two Azure DBs in Use

| Resource Type         | Name / Purpose                  | Contents                                    | Used By (Files)                          |
|----------------------|----------------------------------|---------------------------------------------|------------------------------------------|
| **Azure SQL DB**     | `concussiondb`                  | Structured triage, symptom, stage exports   | `db_models.py`, all `log_*` + `export_to_sql.py` |
| **Azure Blob Storage** | `concussionexports` container | PDF and FHIR bundles for each check-in      | `export_summary.py`, `render_pdf`, `build_fhir_bundle` |

---

## 🧠 Azure SQL DB – Key Facts

- **Created in Portal**: via SQL Database + new SQL Server
- **Connection string**: stored in Railway as `AZURE_SQL_CONNECTION_STRING`
- **Schema setup**:
  - Converted `db_models.py` ORM to raw SQL
  - Executed in Azure Data Studio
- **Query from**: `/export_to_sql`, Power BI, or directly in studio

---

## 📄 Azure Blob Storage – Purpose

- Hosts static files like:
  - `summary_{user_id}.pdf`
  - `bundle_{user_id}.json` (FHIR)
- Created automatically via `render_pdf` and `build_fhir_bundle`
- Files are pushed to Azure Blob via configured connection string

---

## 🛠️ App File Map: Read/Write Access

| File                          | Reads From                | Writes To                 |
|-------------------------------|---------------------------|---------------------------|
| `log_incident_detail.py`     | —                         | Azure SQL: `incident_report_export`        |
| `log_symptoms.py`            | `IncidentReport`          | Azure SQL: `symptom_log_export`           |
| `assess_concussion.py`       | YAML URLs                 | Azure SQL: `concussion_assessment_export` |
| `get_stage_guidance.py`      | TrackerState              | Azure SQL: `stage_result_export`          |
| `export_to_sql.py`           | Local SQLite (default)    | Azure SQL (all exports)   |
| `export_summary.py`          | Azure SQL                 | Azure Blob (PDF, FHIR)     |

---

## ⚙️ Deployment Summary: Azure SQL

### 1. Created Azure SQL DB + SQL Server
- Used SQL Authentication (not Entra)
- Allowed local IP + Azure Services in firewall

### 2. Stored connection string securely
- `AZURE_SQL_CONNECTION_STRING` added to Railway

### 3. Created schema
- Used Azure Data Studio GUI
- Executed SQL equivalent of `db_models.py`

---

## 🧑‍💻 Admin Tool: Azure Data Studio

### 🔹 Features
- Cross-platform SQL client (Mac, Windows, Linux)
- Graphical explorer, query editor, export tools
- Free and lightweight

### 🔹 How To Use
1. Download from: https://learn.microsoft.com/sql/azure-data-studio/download
2. Connect using:
   - Server: `concussiondbserver.database.windows.net`
   - DB: `concussiondb`
   - Auth: SQL Login (e.g. `sqladmin`)
3. Run queries like:
```sql
SELECT * FROM symptom_log_export;
```

---

## 📦 Azure Blob Admin Equivalent

Use **Azure Storage Explorer**:
- Free desktop app from Microsoft
- Browse containers, upload/download files, inspect PDFs

🔗 Download: https://azure.microsoft.com/en-us/products/storage/storage-explorer/

Use it to:
- Inspect `concussionexports` container
- Verify files written by `/export_summary`
- Delete/review historic logs

---

For updates, merge this addendum into `deploy_guide.md` or keep as a linked reference.