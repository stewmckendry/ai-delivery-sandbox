# 🛠️ Task 311: Fix /upload Auth Error for Public Access

## 🎯 Goal
Fix the `/upload` route so that it can be publicly accessed by end users in a browser, even when the rest of the API requires authentication.

---

## 🧩 Problem
- The route `/upload?session=...` now triggers a `422 Unprocessable Entity` when opened in a browser
- Root cause: it uses the shared `require_token` dependency, but browsers do **not send** Authorization headers from GPT links

---

## ✅ Fix Plan
- ✅ Remove the dependency on `require_token` from this route only:

```python
@router.get("/upload", response_class=HTMLResponse)
def upload_form() -> HTMLResponse:
    ...
```

- Keep `/upload/sas` and `/upload/log` secured — they generate upload links and audit logs

---

## 🧪 Test Plan
- Open the URL:
  ```
  https://ai-delivery-sandbox-production-d1a7.up.railway.app/upload?session=<id>
  ```
- Confirm form loads without 401/422 errors
- Confirm uploaded file still goes through SAS upload process (which is secured)

---

## ✅ Done When
- Users can open `/upload` from GPT without auth headers
- SAS and log routes are still protected
- GPT links to `/upload?session=...` now work without failing
