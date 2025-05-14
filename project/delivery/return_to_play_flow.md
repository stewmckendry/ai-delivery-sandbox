# 🧠 Return-to-Play Flow Spec

This document outlines the end-to-end logic and tooling that supports the concussion recovery and return-to-play process.

## 🎯 Goal
Guide users through a structured recovery process following a concussion — based on SCAT6 return-to-play principles — using daily symptom/activity check-ins and intelligent stage guidance.

---

## 🔁 Flow Summary

1. **User experiences head injury → starts triage**
2. **Logs incident details using `/log_incident_detail`**
3. **Assesses concussion risk via `/assess_concussion`**
4. **Receives stage overview from `/get_stage_overview`**
5. **Each day, user attempts a stage activity and logs a check-in via `/log_activity_checkin`**
6. **GPT uses `/get_stage_guidance` to determine current recovery stage based on activity & symptoms**

---

## 🧠 Stage Inference Logic

Stage is inferred by evaluating the latest activity check-in and subsequent symptom severity.

| Scenario | Conditions | Inferred Stage | `inference_mode` | Advice |
|----------|------------|----------------|------------------|--------|
| **No activity check-in** | No activity check-ins in DB | Stage 1 | `no_activity_checkin` | Prompt user to try light aerobic activity and check back in |
| **Symptoms worsened** | Last activity check-in flagged `symptoms_worsened=true` | Prior stage | `regressed_due_to_symptom_worsening` | Revert to safer stage, advise caution |
| **<24h with mild symptoms** | Mild symptoms, but check-in was <24h ago | Current stage | `waiting_period` | Hold current stage, recheck tomorrow |
| **≥24h with mild symptoms** | Mild symptoms, 24h passed since last activity | Next stage | `confirmed` | Promote to next stage |

---

## 🧰 Supporting Tools

### Stage Tracking
- `/log_activity_checkin` → logs the user's activity attempt and if symptoms worsened
- `/get_stage_guidance` → evaluates readiness based on activity and symptoms
- `/get_stage_overview` → educates the user about all stages

### Check-in Management
- `/get_checkin_flow` → returns YAML-driven structure for activity check-ins
- `reference/checkin_map.yaml` → defines check-in questions and formats

### User Data & Continuity
- `/get_user_history` → retrieves past symptoms, activities, and incident data
- `activity_checkin_export` → stores user stage attempts
- `symptom_log_export` → stores all symptom data
- `stage_result_export` → stores recovery stage decisions

---

## 📦 Key Code Files
- `app/tools/get_stage_guidance.py`
- `app/engines/stage_engine.py`
- `app/tools/log_activity_checkin.py`
- `app/tools/get_stage_overview.py`
- `app/models/stage.py`
- `app/db/db_models.py`

---

## 🧪 Testable Outcomes
- User can progress from Stage 1 → Stage 5 via repeated daily check-ins
- GPT explains stage guidance empathetically and contextually
- System handles cold start (no memory) using `get_user_history`

---

_Last updated: 2025-05-13 by QAPod_