# Speed Tactics for WP Pods

This guide helps WP Pods iterate faster across build, deploy, test, and documentation.

---

## 1. Build Phase

### Inline First, Formal Later
- Begin with in-chat implementation of core functions.
- Get user validation inline before committing.
- Only polish and formalize code after proving viability.

### Deliver in Logical Chunks
- Group related deliverables (e.g. tools + models + migrations).
- Don’t wait to finish the entire WP before starting commits or tests.

---

## 2. Shared Utilities

### Identify Shared Components
- Look for models, utils, base classes that span WPs.
- Use common naming conventions to reduce duplication.

### Notify Lead Pod
- When creating shared logic, ping the Lead Pod.
- Lead Pod will notify other Pods and check for dependency coordination.

---

## 3. Documentation

### Document in Parallel
- Start with README-style notes in-chat.
- Add formal docs after code is stable.

---

## 4. Deployment

### Commit Setup Instructions Early
- As soon as code is runnable, commit deployment steps to:
  `project/deploy/wps/<wp_id>/`

### Share CLI Examples
- Even if automation isn’t ready, provide bash or curl commands.

---

## 5. Testing

### Provide Immediate Test Hooks
- For every tool or feature, share basic test command inline.
- Example: curl call to run tool endpoint with mock input

### Commit Test Plans Later
- Store in `project/test/<wp_id>/` once validated.

---

## 6. Async Coordination

### Use Lead Pod for Cross-WP Updates
- Raise blockers or overlapping code to Lead Pod
- Lead Pod ensures updates are propagated

---

## Summary
WP Pods are empowered to:
- Move fast with inline-first approach
- Deliver in commits per logical unit
- Ask for help from Lead Pod or WP12
- Defer polish until after user feedback

This approach keeps momentum high without compromising quality.