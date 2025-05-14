# 🛠️ Return-to-Play Flow Enhancement: Task Tracker

## ✅ Phase 1: Foundation (Complete)
- [x] Refactor `StageLog` to structured fields
- [x] Update `stage_engine.py` to use consecutive mild days
- [x] Improve `StageResult` response with matched_factors
- [x] Add SQL migration for `stage_result_export`

## 🚧 Phase 2: Realistic Stage Progression
- [ ] Add new DB model: `activity_checkin_export`
- [ ] Add SQL schema migration for `activity_checkin_export`
- [ ] New Tool: `log_activity_checkin.py`
- [ ] Update `stage_engine.py` to require activity confirmation
- [ ] Update `get_stage_guidance.py` to surface activity factors

## 🔜 Phase 3: Reusable Daily Check-ins
- [ ] Add new DB model: `checkin_log_export`
- [ ] Add YAML guide: `reference/checkin_map.yaml`
- [ ] New Tool: `log_checkin.py` (replaces `log_symptoms`)
- [ ] Adjust GPT prompts to pull known data (injury date, last check-in)

## 🧭 Phase 4: Education and Summary Tools
- [ ] New Tool: `get_stage_overview.py`
- [ ] Add summary markdown: `project/delivery/stage_guidance_tips.md`
- [ ] Update `openapi.json` with new tools and examples

## 📁 Finalization and Docs
- [ ] Update `project/delivery/return_to_play_flow.md` with full flow spec
- [ ] Create test plan for new tools
- [ ] Document examples for GPT Q&A (how to explain stages)

---

> This tracker lives at: `project/delivery/return_to_play_task_list.md`
> Updated: 2025-05-13
> Owner: QAPod