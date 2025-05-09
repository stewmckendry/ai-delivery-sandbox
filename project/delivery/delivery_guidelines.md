## 🛠️ Delivery Guidelines – Concussion Recovery GPT App (PoC)

This document describes the delivery approach for each feature area, aligned with our mission (Design → Build → Deploy → Test) and the principles defined in project Ways of Working.

---

## 🔁 Task Lifecycle
Each feature will be managed using the delivery platform lifecycle:
- **Create** task with clear scope
- **Log chain of thought** (exploration, decisions, tradeoffs)
- **Commit outputs** as code or documentation is produced
- **Complete task** when all delivery phases are satisfied

---

## 📦 Outputs Per Phase

> For tool testing, use Postman to validate tool behavior before GPT integration.
> This includes endpoint calls, sample inputs/outputs, and schema assertions.
> This helps isolate bugs and speeds up GPT prompt development.

Each phase must include **traceability**:
- Design → references `app_features.md`, `system_architecture.md`
- Build → implements `design.md`
- Deploy → enables integration and real use
- Test → validates expected behavior

| Phase     | Output                                                                 |
|-----------|------------------------------------------------------------------------|
| **Design** | `design.md`: tool flows, schema, instructions, edge cases             |
| **Build**  | Code added to `app/` (tools, engines) + integration notes in feature folder |
| **Deploy** | Central scripts in `project/deploy/` + deployment plan + checklist in feature |
| **Test**   | `test/`: Test plans, pytest cases, Postman collections, results logs  |
| **Docs**   | `README.md`: feature summary, setup, usage, and links to code/tests   |

Each output resides in:
```
project/delivery/features/feature_<N>_<short_name>/
```

---

## 🔨 Feature Delivery Plan

Each feature follows the same structure but with context-specific notes:

### 🧠 Feature 1 – Triage + Assessment
- Uses YAML triage logic, red flag detection
- Tests: flag triggers, tracker creation, GPT routing

### 📅 Feature 2 – Symptom Logging + Stage Inference
- Builds on tracker, uses stage YAML
- Tests: recovery stage correctness, tool chaining

### 📦 Feature 3 – Wearables
- Uses mock API for wearable data
- Tests: ingest + stage guidance adaptation

### 🏥 Feature 4 – Export
- PDF and FHIR summary tools
- Tests: schema conformance, Epic sandbox write

### 📊 Feature 5 – Dashboard
- Azure export and Power BI filters
- Tests: export job, SQL structure, filter accuracy

### ⚙️ Feature 6 – YAML Engines
- YAML parsing, validation, and changelogs
- Tests: schema rules, CI checks, changelog tracking

### 🧪 Feature 7 – Infra + Testing
- Pytest + Postman + logging
- Includes GPT-level metrics + magic link rate limits

### 💡 Feature 8 – UX Enhancements
- Role-based prompts, magic link polish
- Stub integrations (e.g. TeamSnap)

### 🧭 Feature 9 – Agent as App
- Demonstrates generalized form replacement
- Adds new flow, shows domain portability

---

## 🧱 Folder Structure

```
app/                          # Live FastAPI + tools for system
├── main.py
├── routes/
├── tools/
├── engines/
├── models/

project/
├── delivery/
│   ├── features/
│   │   └── feature_<N>_<key>/
│   └── build_phase_backlog.md
├── deploy/
│   ├── local/, azure/, postman/
│   └── README.md
├── prompts/                 # GPT prompt examples + specs
├── tools/                   # OpenAPI schemas
└── test/infra/              # CI, validation, logging

reference/                   # Clinical YAML inputs
```

---

## ⚙️ Principles

- **Front-to-back delivery**: Every feature must function end-to-end from GPT to system
- **Real interface, not mocks**: Build tool, not simulate
- **Prompt + Tool alignment**: GPT behavior is part of tool spec
- **Structured trace**: Reasoning is captured as we go
- **Minimal friction**: Designed for deployability and demo readiness