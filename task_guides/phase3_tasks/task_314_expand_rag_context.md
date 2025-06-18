# 🤖 Task 314: Expand `/ask` Context with Token-Aware Record Selection

## 🎯 Goal
Improve answer accuracy from `/ask` by feeding GPT more than the last 5 records — up to a safe token limit (e.g. ~3,000 tokens).

---

## 🔍 Current Problem
The current `/ask` logic only retrieves:
```python
.limit(5)
```
...for labs, visits, and structured records. This:
- Misses older or abnormal entries
- Prevents GPT from seeing patterns over time
- Leads to shallow answers despite rich record history (60+ entries)

---

## ✅ Proposed Fix
1. **Remove hard `.limit(5)`**
2. **Retrieve all records** for the session
3. **Sort by clinical priority**:
   - Labs by abnormality or recency
   - Visits by recency
   - Structured records by clinical_type and uniqueness

4. **Build the prompt dynamically**:
   - Add records one-by-one to the prompt string
   - Stop once ~3,000 tokens of context are reached (GPT-3.5 safe)
   - Use `tiktoken` or a fast token length estimator

---

## 🧪 Testing
- Use sessions with 50+ records
- Confirm expanded GPT output references older and more diverse entries
- Validate token usage doesn’t exceed model limits

---

## ✅ Done When
- `/ask` returns answers using a deeper, more representative sample of the record set
- Context building is bounded by safe token limits (e.g. 3,000–3,500 tokens)
- Answers improve in coverage, accuracy, and personalization

---

## 💡 Future
- Could extend to support `max_records` or `record_type_filter` as query params