# 🧠 Concussion Recovery App – End-to-End Data Flow Audit (Source of Truth)

This document captures the full pipeline of data flow in the Concussion Recovery App, from user interaction to data persistence and export. It includes structured models, tool mappings, database tables, user flows, and reporting expectations. It also identifies implementation gaps and proposes corrective actions.

...(full content in canvas)...

## 📘 8. Next Steps
- [ ] Implement `TriageResponse` model and table
- [ ] Extend `log_incident_detail.py` to write triage answers to DB
- [ ] Rename reserved `metadata` field → `log_metadata`
- [ ] Optionally log output of `assess_concussion` and `get_stage_guidance`
- [ ] Update Power BI view definitions
- [ ] Replace `data_flow_addendum.md` with this document