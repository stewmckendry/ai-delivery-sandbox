# 🛠️ Return-to-Play Flow Enhancement: Task Tracker

## ✅ Phase 1: Foundation (Complete)
- [x] Refactor `StageLog` to structured fields
- [x] Update `stage_engine.py` to use consecutive mild days
- [x] Improve `StageResult` response with matched_factors
- [x] Add SQL migration for `stage_result_export`

## ✅ Phase 2: Realistic Stage Progression
- [x] Add new DB model: `activity_checkin_export`
- [x] Add SQL schema migration for `activity_checkin_export`
- [x] New Tool: `log_activity_checkin.py`
- [x] Update `stage_engine.py` to require activity confirmation
- [x] Update `get_stage_guidance.py` to surface activity factors

## ✅ Phase 3: Reusable Daily Check-ins
- [x] Add YAML guide: `reference/checkin_map.yaml`
- [x] New Tool: `get_checkin_flow.py`
- [x] Adjust GPT prompts to pull known data (injury date, last check-in)

## ✅ Phase 4: Education and Summary Tools
- [x] New Tool: `get_stage_overview.py`
- [x] Update `openapi.json` with new tools and examples *(manual)*

## 📁 Finalization and Docs
- [ ] Update `project/delivery/return_to_play_flow.md` with full flow spec
- [ ] Create test plan for new tools
- [ ] Document examples for GPT Q&A (e.g., how to explain stages, match activity to stage)
- [ ] Add `project/delivery/stage_guidance_tips.md` *(optional)*
- [ ] Update `get_stage_guidance` to align with activity-checkin logic (fallbacks, strict mode)
- [ ] Update `stage_engine.py` to track fallback scoring method vs confirmed activity path
- [ ] Update GPT system instructions with revised E2E flow logic and Q&A support

---

> This tracker lives at: `project/delivery/return_to_play_task_list.md`
> Updated: 2025-05-13
> Owner: QAPod