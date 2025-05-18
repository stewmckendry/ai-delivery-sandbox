### 🗂️ Recommended Repo Structure for Artifact Governance

This structure reflects best practices learned from past delivery experience and is designed to cover the full SDLC while minimizing artifact sprawl.

---

#### 🧠 Strategy & Discovery
```
project/discovery/              # Vision, goals, personas, user flows
project/acceptance/             # Acceptance criteria, stakeholder success criteria
```

#### ⚙️ Architecture & Design
```
project/system_design/          # Component and architecture diagrams, design principles
project/data_flow/              # Data lifecycle, ingestion, export, flow diagrams
project/schema/                 # Versioned database schema, validation rules
project/tool_catalog/           # OpenAPI tools, route specs, usage contracts
```

#### 🚧 Delivery (Feature or Layer Scoped)
```
project/features/<feature_name>/  # Plan, design, tasks, addendums for each feature
project/deployment/               # Deploy steps, cutover guides, environment configs
project/qa_and_test/              # QA plans, test cases, logs, smoke and staging tests
project/tasks/                    # Optional: tasks scoped outside feature flow
```

#### 📊 Reporting & Integration
```
project/export/                # Dashboard definitions, exports, shaping
project/fhir/                  # FHIR bundles, mappings, validation
project/analytics/             # Metrics, cohort shaping, anonymization
```

#### 📓 Logs & Metadata
```
.logs/issues/                  # Framework issues, enhancement proposals
.logs/retros/                  # Retrospectives per phase/feature
project/memory.yaml            # Canonical file index with tags
project/changelog.yaml         # File-level commit history
```