# Task 18 Review: Credential Input UI Stub

## ✅ Summary
Implements a Markdown-based pseudo-form to illustrate credential capture for a health portal login.

## 📂 File
- `task_guides/ui_stub/credential_input.md`

## 📋 Content
- Form fields for portal, username, and password
- Sample HTML with a simulated submit button
- Backend usage example calling Redis for temporary credential storage

## 🔄 Reuse
- Mentions `app/storage/redis.py` as the expected target for real implementation

## 🧪 Test
- Not a code module — no functional test required
- ❌ `pytest` failed due to unrelated collection error

## 📷 Sample Snippet
```html
<form>
  <label for="portal">Portal Name</label>
  <input id="portal" type="text" placeholder="e.g. Portal A" />
...
```

## 💬 Feedback
- ✅ Useful visual prompt for ChatGPT-enabled input collection
- ✅ Clearly communicates how real inputs would be handled

## 🚀 Ready for integration into ChatGPT flows or future UI wiring