## Integration Points (v2)

This document summarizes all system integration points for PolicyGPT. Each integration supports one or more core flows: document ingestion, planning, reasoning, knowledge enrichment, document validation, export, and system auditability.

---

### 🔗 Primary Integration Layers

| Integration           | Description                                                               | Protocol / Tech       | Status     |
| --------------------- | ------------------------------------------------------------------------- | --------------------- | ---------- |
| **Google Drive**      | Stores final documents and user-submitted sources for ingestion           | Google Drive API      | ✅ Active   |
| **Airtable**          | Hosts structured project profiles and business case metadata              | Airtable REST API     | ✅ Active   |
| **ChromaDB**          | Embedding-based semantic search over reference material and prior cases   | Local ChromaDB API    | ✅ Active   |
| **OpenAI GPT-4**      | Language model used for planning, drafting, tool chaining, and refinement | OpenAI API            | ✅ Active   |
| **Web Search**        | Real-time information retrieval to augment citations                      | DuckDuckGo API        | 🔄 Planned |
| **PostgreSQL**        | Stores all draft, audit, trace, and memory data                           | psycopg2 / SQLAlchemy | ✅ Active   |
| **GitHub (optional)** | Project version control or artifact tracking                              | GitHub API (v3)       | 🔄 Planned |

---

### 🧠 GPT Integration Pattern

GPT is used in 4 key roles:

1. **Planner** – Creates task and toolchain based on `gate_reference.yaml`
2. **Tool Invoker** – Recommends tools to run, but FastAPI handles execution
3. **Critic + Validator** – Audits outputs and suggests follow-ups
4. **Composer** – Writes content using `compose_and_cite` and reasoning memory

**Execution Flow:**

```
User prompt → GPT planner creates task →
Toolchain proposed → FastAPI executes tools (via OpenAPI) →
Results reviewed by GPT → Human feedback loop → Commit/export
```

* All GPT calls are logged to `PromptLog`
* Planner and toolchain traces saved to `ReasoningTrace`
* Tool output and edits saved to `ArtifactSection`, `AuditTrail`

---

### 📥 Ingestion Points

| Source              | Format          | Handling Module        | Notes                                  |
| ------------------- | --------------- | ---------------------- | -------------------------------------- |
| Uploaded Docs       | PDF, DOCX       | `upload_and_parse`     | Converted to Markdown + indexed        |
| Reference Templates | Markdown / YAML | `load_template`        | Used by planner + compose tools        |
| Airtable Profiles   | Structured JSON | `query_airtable`       | Used to populate section drafts        |
| Gate Requirements   | YAML            | `load_gate_reference`  | Used to initialize planner task        |
| Project Profile     | YAML            | `load_project_profile` | Central fact base across all artifacts |

---

### 📤 Output and Export

| Target               | Format         | Trigger             | Notes                                     |
| -------------------- | -------------- | ------------------- | ----------------------------------------- |
| Google Drive         | DOCX, PDF, MD  | `commit_and_export` | Final output committed + metadata stored  |
| GitHub (optional)    | Markdown, YAML | `push_commit`       | For external version control (if enabled) |
| Local YAML Snapshots | YAML           | `session_store`     | For memory continuity + cache fallback    |

> 📌 All large documents are assembled post-hoc from individual sections to avoid token limit issues. Project-wide facts in `project_profile.yaml` minimize repeated prompt context. Final review and storage occurs outside GPT (Drive or GitHub).

---

### 🔁 Data Exchange Patterns

| Between         | Protocol       | Format | Purpose                                 |
| --------------- | -------------- | ------ | --------------------------------------- |
| GPT → Tools     | OpenAPI / REST | JSON   | Structured tool invocation and chaining |
| Tools → FastAPI | Python / REST  | JSON   | Processing and validation               |
| FastAPI → DB    | SQLAlchemy     | SQL    | Persistence of all session + audit data |
| FastAPI ↔ GPT   | REST           | JSON   | Dynamic prompting, response validation  |

---

### 🔐 Authentication Flows

* **Google Drive:** OAuth with service account and delegated scopes
* **Airtable:** API Key + base-specific token
* **OpenAI / Web Search:** API Key from secure vault
* **DB Access:** Role-based credentials using environment variables

> 🔐 All secrets managed via `.env` and deployed using Railway environment variables

---

### 📂 GitHub vs. Local YAML

| Store      | Purpose                                         | Format   |
| ---------- | ----------------------------------------------- | -------- |
| GitHub     | Optional artifact audit trail + delivery log    | Markdown |
| Local YAML | Active session memory, tool metadata, snapshots | YAML     |

GitHub stores long-term snapshots of outputs for compliance, while local YAMLs support tool execution, session recall, and memory syncing.

---

### 🧾 Actions to Implement

* [ ] Add web search plugin support (fallback for `search_knowledge_base`)
* [ ] Build GitHub integration to track generated artifacts (optional)
* [ ] Add OAuth flow for user-authenticated Drive access (if needed)
* [ ] Enable tool chaining middleware for advanced planner-agent flows
* [ ] Ensure DB error logs are exported for external monitoring dashboard
* [ ] Define schema + usage flow for `project_profile.yaml`
* [ ] Ensure per-section planning → export assembly adheres to token-safe strategy
* [ ] Add doc-level GPT feedback handling flow with retry/validate support
