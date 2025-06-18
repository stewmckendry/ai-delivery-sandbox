# 🔐 Task 308: Privacy and Security Review of AI Health Copilot Stack

## 🎯 Goal
Conduct a holistic review of the application's privacy and security posture across all components:
- GPT frontend (MyHealth Copilot)
- Operator collection
- FastAPI backend
- Azure Blob & SQL storage

Identify improvements to ensure safe handling of personal health data, especially in cloud or public deployment scenarios.

---

## 🔍 Review Scope

### GPT Layer (ChatGPT + Custom GPT)
- How is session context scoped and isolated?
- Is a consistent session_key used per user?
- Are GPT outputs ever exposed to third-party plugins?

### Operator + Collection
- Do Operator sessions leave residual files?
- Are credentials ever cached?
- Can Operator link be limited or shortened for session control?

### FastAPI Backend
- Is HTTPS enforced end-to-end?
- Do APIs validate input and authenticate user sessions?
- Are summaries or audit logs persisted unnecessarily?

### Azure Blob / SQL
- Are blob storage containers using private access + SAS URLs?
- Are SQL records only keyed by session, without personal identifiers?
- Are expiration or retention policies in place?

---

## 🛠 Task Scope
- Review `app/api/*.py`, `orchestrator.py`, storage layers
- Assess access controls on all public-facing routes
- Recommend:
  - Secure defaults (e.g., blob expiry, header validation)
  - Optional enhancements (e.g., auth tokens, audit flags)
  - Documentation for end users about data safety

---

## ✅ Done When
- Summary report lists current practices and areas for improvement
- Specific file/code references are cited for each risk/opportunity
- At least 3 security/privacy improvements are proposed, with reasoning