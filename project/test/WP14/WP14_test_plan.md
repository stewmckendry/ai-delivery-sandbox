## WP14 Test Plan: External Search Tool

### 🎯 Objectives
- Verify the `webSearch` tool runs for each supported search type
- Confirm fallback logic in `generate_section_chain.py` when memory is empty
- Validate API output structure matches expected schema
- Ensure logs are written to `WebSearchLog`

---

### ⚙️ Setup Steps
1. Set `.env` variable:
   ```env
   BING_API_KEY=your_rapidapi_key_here
   ```
2. Ensure the following dependencies are installed:
   ```bash
   pip install requests python-dotenv
   ```
3. Verify toolchain is on branch: `sandbox-curious-falcon`

---

### 🧪 Test Runs
Each test runs `webSearch` via planner for a distinct `search_type`.

#### Test 1: General Web Search
- **Input:**
  ```json
  {
    "intent": "external_web_search",
    "inputs": {
      "query": "digital ID infrastructure",
      "search_type": "general"
    }
  }
  ```
- **Expected:** 3+ results with keys: `title`, `snippet`, `url`

#### Test 2: Jurisdictional Search
- **Input:**
  ```json
  {
    "intent": "external_web_search",
    "inputs": {
      "query": "digital ID",
      "search_type": "jurisdiction",
      "context": {"location": "Canada"}
    }
  }
  ```
- **Expected:** Results scoped to `.gov`, `.gc.ca`, `.gov.uk` domains

#### Test 3: Market Search
- **Input:**
  ```json
  {
    "intent": "external_web_search",
    "inputs": {
      "query": "identity verification",
      "search_type": "market",
      "context": {"industry": "financial services"}
    }
  }
  ```
- **Expected:** Commercial/vendor examples returned

#### Test 4: Section Chain Fallback
- **Input:**
  ```json
  {
    "intent": "generate_section",
    "inputs": {
      "artifact": "test_artifact_001",
      "section": "security",
      "gate_id": "G1",
      "project_id": "TEST_PROJECT",
      "session_id": "s1",
      "user_id": "u1"
    }
  }
  ```
- **Expected:** If memory is empty, `webSearch` is invoked and returns results

---

### 📥 Required Data
- Insert a test project profile into DB:

```sql
INSERT INTO project_profile (project_id, project_name, org) 
VALUES ('TEST_PROJECT', 'Test Project', 'Example Org');
```

- Or skip DB write and mock this via `context` if DB not available

---

### 📌 Notes
- All tests should print the returned results
- Log entries can be checked in the `web_search_logs` table
- Test runner will automate all 4 test cases