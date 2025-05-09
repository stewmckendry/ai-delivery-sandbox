## 🧠 Spike Report: Session Memory Linking in GPT – Concussion Recovery GPT App

---

### 🎯 Objective
Explore how the app can persist user session memory across multiple GPT interactions (e.g., symptom tracking, return-to-play). This allows a parent or coach to return later and resume an ongoing recovery tracker.

---

### 🧩 Problem Statement
- GPT sessions are stateless unless memory is explicitly passed or stored
- Need to link return visits to an existing `tracker_id`
- Session handoff between GPT and backend must be secure, seamless, and usable by non-technical users

---

### 🔐 Memory Key Options

#### Option 1: Human-readable Tracker Code
- Upon tracker creation, GPT returns a short code (e.g., `TRK-8312`) and tells user to save it
- On return, user is asked to re-enter the code

✅ Simple, secure
❌ Manual effort; risk of lost code

#### Option 2: Magic Link via Email or Bookmark
- GPT offers to email or generate a clickable recovery link
- Link contains signed token (JWT or UUID)

✅ Easy for users, good UX
❌ Email not always available; more setup needed

#### Option 3: Device-level Session Memory
- Store token locally via GPT Custom GPT session memory

✅ Zero friction if used in same browser
❌ Not portable; erased on logout or new device

---

### 📦 Backend Tracker Persistence
Trackers are stored in the backend DB:
```json
{
  "tracker_id": "uuid",
  "user_id": "anon-xyz",
  "incident_date": "2025-05-01",
  "sport": "soccer",
  "age": 14,
  "gender": "female",
  "symptoms": [...],
  "recovery_stage": "stage_2",
  "last_checkin": "2025-05-04"
}
```

---

### 🔁 GPT ↔ Backend Handoff

**Tracker Creation Flow**:
1. GPT calls `create_tracker`
2. Backend returns `tracker_id` + optional `link`
3. GPT gives user a reminder and guidance to save it

**Tracker Resume Flow**:
1. GPT asks for tracker code or link (or auto-fetch from memory)
2. Calls `get_tracker_status(tracker_id)`
3. Resumes daily check-in flow

---

### 📌 Recommendation
- Support both **short code fallback** and **magic link** options
- Always show user the `tracker_id` and let them copy/bookmark it
- If using Custom GPT memory, store `tracker_id` and surface on session resume

---

### ✅ Next Steps
- Define token format and expiration for magic links
- Add `resume_tracker(tracker_id)` endpoint
- Update GPT instructions to save and reuse memory if available
- Add helper tool `get_tracker_by_code` for returning users

---