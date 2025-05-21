### 🧪 WP3b Test Plan — Tool Registry + API

This test plan verifies that the Tool Registry system is working end-to-end across CLI, API, and GPT manifest interfaces.

---

### 🔧 Environment
- Railway URL: `https://robust-adventure-production.up.railway.app`
- Local FastAPI: `http://localhost:8000`

---

### ✅ Test Scenarios

#### 1. **Health Check**
- [ ] `GET /status`
- **Expected:** `{ "status": "ok" }`

#### 2. **Tool Manifest**
- [ ] `GET /tools`
- **Expected:** list of 18 tool entries with schemas and metadata

#### 3. **Tool Validation Pass**
- [ ] `POST /tools/translateDocument`
```json
{
  "target_lang": "fr",
  "doc_text": "this is a test"
}
```
- **Expected:** stubbed success message from tool

#### 4. **Tool Validation Fail**
- [ ] `POST /tools/translateDocument`
```json
{
  "doc_text": "this is a test"
}
```
- **Expected:** error for missing required `target_lang`

#### 5. **GPT Tool Manifest Format**
- [ ] Load `/project/reference/gpt_tools_manifest.json`
- **Expected:** valid OpenAPI-compliant manifest with 18 tool paths and schemas

---

### 📁 Data Pack
Included inline above (can also be scripted via Postman or curl). No DB or secrets required.

---

### ⏭ Next
- Run tests (local and Railway)
- Record outcomes in `test_summary.md`
- Raise any failures as issues in WP3b or defer to owning WPs