## 🤖 GPT User Flow – Drive Integration (WP20)

This document illustrates how GPTs, users, and Drive integration interact across PolicyGPT workflows.

---

### 🧭 Scenario A – Draft to Drive (E2E Generation)

1. **User** finishes validation of draft sections
2. **Planner Toolchain** calls `assemble_artifact`
3. **GPTs** finalize markdown (metadata, version, etc.)
4. `storeToDrive.py` is triggered
   - Markdown → PDF
   - Uploaded to Drive
   - Drive URL saved to DB
5. **User** receives link to review or distribute

📥 Input: gate ID, artifact ID, version, markdown  
📤 Output: PDF file on Drive + link saved to DB

---

### 📤 Scenario B – Upload + Fetch

1. **External reviewer** updates document in Drive
2. **User or GPT** wants to pull latest version
3. `fetchFromDrive.py` is triggered with metadata
4. PDF is located via Drive search
5. **Link returned** to user or tool

🔁 Enables manual-to-automated document loops

---

### 🧪 Scenario C – Revisions + Regeneration

1. **User** requests revised version based on feedback
2. GPT compares retrieved PDF (via Drive link)
3. Differences extracted → used for rewrite or version bump
4. Updated PDF committed to Drive again

---

### 🧠 Key Roles
- **GPTs**: Compose, finalize, diff, or re-import docs
- **Users**: Review, distribute, externally update
- **Planner Toolchains**: Trigger Drive actions post-validation or pre-fetch

---

### 🔐 Access + Auth UX
- Service account manages file ownership
- Folder shared with user base (admin controls)
- URLs can be previewed directly in chat or embedded in UI

---

✅ This flow ensures full-circle drafting, feedback, and storage lifecycle through Drive.