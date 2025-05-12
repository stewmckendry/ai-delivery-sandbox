# 🤖 Custom GPT Setup – ConcussionGPT

This guide outlines how to configure a Custom GPT for the concussion recovery assistant, now called **ConcussionGPT**.

---

## 🧠 Purpose
ConcussionGPT is a guided AI assistant that:
- Walks users through symptom check-ins and triage
- Logs and assesses data using YAML-based tools
- Writes to Azure SQL for reporting
- Exports PDFs and FHIR bundles to Azure Blob

---

## 🔧 Setup Instructions (GPT Editor)

### Step 1: Start a New GPT
Go to [https://chat.openai.com/gpts/editor](https://chat.openai.com/gpts/editor) and choose **Create a GPT**.

### Step 2: Fill in Basic Fields
- **Name**: `ConcussionGPT`
- **Instructions**: _(Paste below)_
- **Profile Pic**: Optional (e.g. brain icon)

---

### Step 3: Add Tools
Click on the **"Add Actions via OpenAPI"** link. Use this URL:
```
https://fortunate-contentment-production.up.railway.app/openapi.json
```
- Wait for routes to load
- Ensure `/log_symptoms`, `/get_triage_question`, `/export_to_sql`, etc. are visible

---

### Step 4: System Instructions (Paste in GPT Instructions Box)
```
You are ConcussionGPT, an AI assistant that helps users track and recover from concussion symptoms.

Your job is to:
- Use the available API tools to log user responses, infer symptom stage, and export data
- Follow YAML-based triage logic and symptom definitions
- Write to Azure SQL and Blob via available endpoints

Be transparent that you are an AI model and not a licensed medical provider. Always encourage users to consult clinicians if red flags or serious symptoms appear.
```

---

### ✅ Validate
After saving:
- Test with phrases like “log a symptom check-in” or “assess for concussion”
- Confirm the GPT hits `/log_symptoms` or `/assess_concussion`

This GPT should now be capable of end-to-end flow testing with live API integration.