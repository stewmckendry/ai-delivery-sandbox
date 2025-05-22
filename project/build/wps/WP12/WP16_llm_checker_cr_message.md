### 🧠 Proposed CR: LLM-Powered Input Completeness Checker

**From:** WP16Pod  
**To:** Pod Lead / WP12 (Design Patch)

---

### 📌 Context
WP16 is currently implementing `inputChecker`, a tool that assesses whether required inputs have been collected for a gate → artifact → section.

The current version (MVP) uses a rules-based approach:
- Compares required intents in `gate_reference_v2.yaml` to user-submitted inputs in `PromptLog`
- Detects missing or empty inputs

---

### ✨ Proposed Enhancement
Introduce an LLM-powered mode that:
- Uses GPT-4 to assess clarity, vagueness, and completeness of free-form answers
- Flags responses that are:
  - Too short, vague, or generic
  - Contradictory or poorly justified
  - Misaligned with evaluation criteria

---

### 🔄 Implications
- Requires a ReAct-style prompt to guide GPT in evaluating answers
- Adds scoring or annotation layer on top of existing completeness report
- Could be triggered as part of review workflow before drafting

---

### ⏭️ Recommendation
Defer LLM-enhanced `inputChecker` to a future WP (e.g. WP6 or WP12 follow-on) and track this capability in roadmap.

No impact on WP16 timeline if accepted as deferred enhancement.

---

Let us know if you’d like us to prototype this during WP16, or mark as follow-on.