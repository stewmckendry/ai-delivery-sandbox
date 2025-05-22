### 🚨 WP16 CR – Input Mode Handling for Custom GPT

**To:** Pod Lead  
**From:** WP16Pod  
**Subject:** Mode-Aware Input Flow Design for PolicyGPT Chat UI  

---

### 📌 Context
PolicyGPT users must choose between two distinct input modes:
- **Guided Mode** – Step-by-step prompts for structured input
- **Data Dump Mode** – Upload files/links/raw text in bulk for later extraction

WP16 is responsible for designing the Input UX Layer that supports both flows.

However, because PolicyGPT runs in the **OpenAI Custom GPT** chat UI, there are **no built-in UI controls** (e.g., toggles or buttons) for mode selection.

---

### 🔍 Recommendation
Use GPT system prompt + conversation starters to handle input mode selection:
- Add clear mode descriptions in the system prompt
- Provide clickable conversation starters like:
  - “Walk me through step-by-step”
  - “I’ll upload everything upfront”
- GPT infers mode from user's starting message and stores it in session metadata

---

### 🛠 Change to WP16 Scope
✅ Document mode-aware behavior in UX design  
✅ Define GPT system prompt snippet and conversation starter examples  
✅ Provide note and metadata handling guidance

---

### 🔜 Spillover Work (Outside WP16)
- Configure **Custom GPT system prompt + starter messages** (likely owned by GPT config Pod)
- Coordinate with **Memory/Infra Pods** to track mode in session context

---

### ✅ Impact
This CR ensures a user-friendly, mode-aware experience without requiring UI controls unavailable in OpenAI ChatGPT. It also allows for consistent session handling across both guided and data dump flows.