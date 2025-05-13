# 🧱 System Design Template – Best Practice

## 📌 Overview
Describe what this system is intended to do, its users, and high-level responsibilities.

- **Purpose:**
- **Key Users:**
- **Scope:**
- **External Integrations:**

## 🧭 Architecture Diagram
Include or link to a diagram that shows the major components and their relationships.

```
[User] → [GPT Layer] → [FastAPI Tools] → [Engines] → [DB Models] → [SQL DB / External]
```

## 🧩 Component Breakdown
| Component        | Role / Function                                           |
|------------------|------------------------------------------------------------|
| GPT Layer        | Frontline interaction, YAML triage, invokes tools         |
| FastAPI Tools    | Route handlers exposed via OpenAPI                        |
| Engines          | Core logic (triage, stage, validation, FHIR)              |
| DB Models        | ORM schema definitions, mapped to export tables           |
| Reference Files  | YAML or CSV configuration for structured flows            |
| SQL DB           | Azure-hosted, stores normalized logs                      |
| Exports          | Dashboard views, PDFs, FHIR bundles                       |

## 🔐 Security Considerations
- How is user data protected?
- What access controls are applied?

## ⚙️ Operational Requirements
- Hosting & environment setup
- Monitoring or alerting needed
- Staging vs prod behavior differences

---
Add links to supporting docs, OpenAPI spec, YAML files if needed.