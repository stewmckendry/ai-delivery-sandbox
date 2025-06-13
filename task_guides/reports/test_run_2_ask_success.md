# 🧠 Test Run 2 (ASK Phase) – test_portal_b

## 🧪 Command
```bash
python scripts/ask_tool.py --query "Summarize all my recent visits and test results."
```

## 📄 Summary
- ✅ Loaded records from: `health_data.db`
- ✅ Queried:
  - Labs: 2
  - Visits: 1
  - Structured Records: 5
- ✅ Sent structured context to OpenAI
- ✅ Received and printed summarized response

## 🧠 Sample Response
```
- Hemoglobin tested on 2023-05-02 showed a level of 13.5 g/dL.
- Cholesterol tested on 2023-05-01 was 5.8 mmol/L.
- Visited Dr. Jones at General Hospital on 2023-06-01 for a routine check.
- Billing information indicates a due date of 2023-07-01 with a balance of $100.
- Lab results for home visits can be downloaded from /tmp/test_b_billing_4c099dec.html.
- Billing summary can be accessed from /tmp/test_b_billing_4c099dec.html.
- Lab results for Hemoglobin test on 2023-05-02 can be viewed at /tmp/test_b_labs_4c099dec.html.
```

## 📊 Context Stats
- Labs: 2
- Visits: 1
- Structured: 5

## 💬 Feedback
- ✅ Excellent blend of structured + AI content
- ✅ Includes source paths for traceability
- 🟡 Optional: group similar items or remove duplicates

## ✅ ASK tool fully operational – user queries can now retrieve and explain health data conversationally.