## API Contracts (v2)

This document defines the API interface exposed by the PolicyGPT backend for use by the custom GPT agent, web client, and integrations. It reflects v2 design updates for planner-based task flow, session memory syncing, audit trail persistence, and dynamic document generation.

---

### 📘 OpenAPI Specification

* **Version:** 2.1 (GPT Tool-Ready)
* **Base URL:** `/tasks` for tool access, `/system` for memory and control
* **Format:** Follows RESTful design + OpenAPI 3.1 schema
* **Tool Contract:** Each tool has required `input` fields and defined `output` schema for GPT validation

---

### 🧰 Core Task Tool Endpoints

| Route                          | Method | Purpose                                         |
| ------------------------------ | ------ | ----------------------------------------------- |
| `/tasks/create_planner_task`   | POST   | Initialize a planner-driven document task       |
| `/tasks/fetch_gate_metadata`   | GET    | Get sections required for a gate/artifact combo |
| `/tasks/fetch_examples`        | GET    | Return gold star exemplars for a given section  |
| `/tasks/compose_and_cite`      | POST   | Generate draft with citation trace              |
| `/tasks/validate_section`      | POST   | Validate a section for factual or logical gaps  |
| `/tasks/commit_and_log_output` | POST   | Save output to YAML + log reasoning trace       |

#### 🧠 Example: `/tasks/compose_and_cite`

```json
{
  "repo_name": "ai-delivery-sandbox",
  "task_id": "2.2_build_and_patch",
  "section_name": "Risk Management",
  "inputs": {
    "context": "...",
    "facts": ["..."],
    "citations": ["url1", "url2"]
  }
}
```

**Output**

```json
{
  "draft_text": "...",
  "citations_used": ["url1"],
  "reasoning_steps": ["fact matched", "risk categorized"]
}
```

---

### 🧠 Session + Memory Management

| Route                         | Method | Purpose                                       |
| ----------------------------- | ------ | --------------------------------------------- |
| `/system/sync_session_memory` | POST   | Upload session YAML to long-term memory store |
| `/system/fetch_session`       | GET    | Return prior session memory if it exists      |
| `/system/describe_file`       | POST   | GPT tool to describe + tag a file for memory  |
| `/system/index_memory`        | POST   | Manually (re-)index project memory            |

---

### 📖 Knowledge + Reference Tools

| Route                       | Method | Purpose                              |
| --------------------------- | ------ | ------------------------------------ |
| `/knowledge/search_kb`      | POST   | Search internal reference files      |
| `/knowledge/query_airtable` | POST   | Query project profiles               |
| `/knowledge/web_lookup`     | POST   | Conduct external search (if enabled) |

---

### 🧾 Planner Trace + Audit

| Route                           | Method | Purpose                                     |
| ------------------------------- | ------ | ------------------------------------------- |
| `/trace/fetch_reasoning_trace`  | GET    | Returns steps and GPT reasoning per section |
| `/trace/fetch_chain_of_thought` | GET    | Return past thoughts and prompts for a task |
| `/trace/log_issue_or_lesson`    | POST   | Append a known issue or learning            |
| `/trace/update_task_metadata`   | POST   | Modify a task's planner metadata            |

---

### 📤 Output + Export

| Route                     | Method | Purpose                                       |
| ------------------------- | ------ | --------------------------------------------- |
| `/export/export_summary`  | POST   | Exports current state as printable summary    |
| `/export/export_artifact` | POST   | Commits section and builds downloadable files |
| `/export/generate_bundle` | POST   | Zip entire run folder for archival/download   |

---

### 🔐 Authentication

* Current mode: None (trusted GPT caller only)
* Future: Signed tokens or per-user key for enterprise edition

---

### ✅ Next Actions

* [ ] Add `/tasks/auto_toolchain_run` to trigger planner-led multi-tool flows
* [ ] Add error status return field for each tool for GPT fallback management
* [ ] Add GPT-detectable output validation schema on all compose + validate tools
* [ ] Group OpenAPI tool definitions by phase (e.g., Plan, Draft, Validate, Export)
* [ ] Publish OpenAPI JSON spec to hosted `/openapi.json` for GPT consumption
