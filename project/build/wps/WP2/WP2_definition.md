## WP ID: WP2
## WP Name: Document Commit + Audit Logging

### 🌟 Outcome
By the end of this WP, as a **policy system**, I will be able to commit finalized policy documents, capture version history, and log all relevant audit trails and approval states. This ensures **traceability**, **accountability**, and **regulatory compliance**.

### 🧽 Scope
**In Scope:**
- Committing documents and metadata to persistent storage
- Logging approval flows and audit events
- Exporting errors from failed commit attempts
- Logging and handling commit failures (esp. external systems like Google Drive)

**Out of Scope:**
- Actual Google Drive document commit, search, or retrieval (moved to WP13)
- Document feedback loops (covered in WP11)
- Scaffolding and section logging (WP1a/WP1b)

### 📦 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/db/models/DocumentVersionLog.py` | Tracks submitted document versions and timestamps. |
| `app/db/models/AuditTrail.py` | Records audit events like commit triggers and system-level changes. |
| `app/db/models/ApprovalLog.py` | Captures reviewer decisions with context. |
| `app/tools/db_error_exporter.py` | Handles extraction of failed commits/errors. |
| `app/utils/log_commit_failure.py` | Centralized handler to record drive/API commit issues. |
| `app/db/schema_migrations.sql` | Updates DB schema with required models. |

### 📄 Supporting Documentation (to generate)
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WP2/WP2_design.md` | Details commit and approval logging flow. |
| `project/build/wps/WP2/WP2_deployment.md` | Instructions for applying schema + deploy checklist. |
| `project/build/wps/WP2/WP2_tests.md` | Unit and integration testing plan. |

### ✅ Acceptance Criteria
- [ ] Submitting a document logs a version to DB.
- [ ] Approval flow changes are captured in `ApprovalLog`.
- [ ] AuditTrail entries created for all key events.
- [ ] Errors during commit are logged and exportable.
- [ ] DB schema migrations deploy cleanly and tables are queryable.

### 🛠 Tasks
| Task ID | Description |
|---------|-------------|
| T1 | Implement `DocumentVersionLog.py` model |
| T2 | Implement `AuditTrail.py` + `ApprovalLog.py` models |
| T3 | Add schema changes to `schema_migrations.sql` |
| T4 | Create `log_commit_failure.py` with retry + log hooks |
| T5 | Create `db_error_exporter.py` for structured error review |
| T6 | Write tests and deploy to dev |

### 📚 Reference Documentation
| File Path | Usage |
|-----------|--------|
| `acceptance_criteria v2.md` | Submission, approval, and traceability requirements |
| `system_architecture_v2.md` | Audit + commit system handoff specs |
| `tool_catalog_v2.md` | Tool logging responsibilities |
| `integration_points_v2.md` | Google Drive integration points |
| `session_memory_model_v2.md` | Long-term memory targets |

### 📝 Notes to Development Team
- Audit and approval logs should be extensible for additional reviewer types.
- Log entries must be timestamped and include actor/system origin.
- `log_commit_failure.py` should include fallback path for reattempt.
- Prepare error logs to include Google Drive commit failures.

---

### 🔍 Clarification Notes

**Commit Targets:**
- ✅ SQL DB: Metadata, audit logs, version tracking
- ✅ Google Drive: Final rendered document upload for long-term storage

**Google Drive Integration:**
- WP2 only handles logging failures to Drive
- Actual Drive I/O tools (commit, fetch, search) are handled in **WP13**

**Drive Logging vs. Write Functions:**
- `log_commit_failure.py` logs issues when Drive upload fails
- A new tool `drive_commit.py` (in WP13) will actually write the file

**Reasoning Trace:**
- Stored in WP1b/1a scope
- Not the focus of this WP
