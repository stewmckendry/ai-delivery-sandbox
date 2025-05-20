# Speed Tactics for WP Pods

To deliver work packages fast *without sacrificing quality*, use the following tactics:

---

## 1. **Batch Early Commits**

- **Don't wait to finish the whole WP** before committing.
- Commit individual deliverables as they’re ready (e.g., one tool or model at a time).
- **Share the GitHub link** for each file to request feedback quickly.

> This allows parallel progress — user reviews your code while you continue building.

---

## 2. **Inline Plan + Design** (No Heavy Specs)

- Share your plan in markdown or comments.
- Highlight **assumptions**, **logic flow**, and **open questions**.
- Ask for approval before coding if major logic is uncertain.

> "Lightweight plans > full specs" helps you start building faster.

---

## 3. **Declare Shared File Changes**

- Call out if you're touching files that may be used by other Pods (e.g., `tool_registry.py`, `memory_sync.py`).
- Add a note in your **status update to Lead Pod**.
- Lead Pod will notify others and coordinate as needed.

> Shared changes = higher coordination need. Flag early!

---

## 4. **Always Reuse Utilities**

- Before creating new utils or models, **check existing tools** in:
  - `app/tools/`
  - `app/utils/`
  - `app/db/models/`
- Ask Lead Pod if unsure what's available.

> Prevent duplicate logic and redundant tools.

---

## 5. **Post-Deploy + Test Fast Handoff**

- After building:
  - Create **deployment instructions** and commit to `project/deploy/wps/<wp_id>/`
  - Create **test cases/scripts** and commit to `project/test/<wp_id>/`
- Await user test results and update as needed.

> This makes your WP immediately usable — no delays post-build.

---

## 6. **Escalate Uncertainty Early**

- If you're unsure about scope, logic, or impact:
  - **Raise it in your WP Pod status update** to Lead Pod.
  - Lead Pod will route to WP12 for design alignment or user for decision.

> Better to clarify now than rewrite later.

---

**For questions or blockers, always route through the Lead Pod.**

Happy shipping!