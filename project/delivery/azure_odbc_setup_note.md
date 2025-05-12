# 🧩 Azure SQL ODBC Connector Setup (Railway Fix)

This note documents how the team resolved a platform-specific deployment error when using `pyodbc` with Azure SQL on Railway.

---

## 🧠 Issue

```
ImportError: libodbc.so.2: cannot open shared object file: No such file or directory
```

Root cause: while `pyodbc` was installed via `requirements.txt`, the underlying **ODBC system drivers** were missing in the Railway build container.

---

## 🔧 Solution: Custom Dockerfile

A custom `Dockerfile` was added to the root to replace Nixpacks and:
- Install Python 3.12
- Install `unixodbc-dev`, `libodbc2`, and Microsoft's `msodbcsql18` driver
- Install app requirements via `pip`

### ✅ Relevant Commands
```Dockerfile
apt-get update && \
apt-get install -y curl gnupg2 apt-transport-https unixodbc-dev libodbc2 && \
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
apt-get update && \
ACCEPT_EULA=Y apt-get install -y msodbcsql18
```

---

## ✅ Outcome
- Railway build now runs successfully
- `/export_to_sql` and all SQLAlchemy calls using Azure SQL + pyodbc function correctly
- Fix logged in `Dockerfile` and tested in branch `sandbox-silver-tiger`

This approach can be reused in future pods requiring `pyodbc` or other binary dependencies.