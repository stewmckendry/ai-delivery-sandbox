## 🚀 Deployment Architecture – CareerCoach MVP

... *(existing content preserved)* ...

---

### 🔐 API Key Security for Custom GPT

CareerCoach’s backend is protected with a Bearer token using an `Authorization` header.

#### ✅ Setup Steps

1. **Define the Key Locally or in Railway**
   - Add to `.env` (for local dev):
     ```
     API_KEY=your-secret-token
     ```
   - Add to Railway **Environment Variables** tab:
     - Key: `API_KEY`
     - Value: (same token as above)

2. **FastAPI Token Middleware (Preconfigured)**
   - Defined in `project/app/utils/auth.py`
   - Applied to all routers via `main.py` using:
     ```python
     dependencies=[Depends(verify_token)]
     ```

3. **Set Up GPT with Token**
   - In GPT Builder under **Actions → Authentication**:
     - Type: **Header**
     - Key: `Authorization`
     - Value: `Bearer your-secret-token`

This ensures only authorized calls from CareerCoach-GPT can access FastAPI tools.

---