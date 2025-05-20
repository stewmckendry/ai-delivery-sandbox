## 🧠 PolicyGPT Lessons Learned Log

### 💡 Lesson: Preventing File Truncation in Commits

**Issue:**
During large file commits (like the Work Package Overview), only the visible portion in the canvas was committed, resulting in truncated files and data loss.

**Root Cause:**
Canvas renders only part of a long document. If the commit references only what's visible, it fails to include the full in-memory content.

**Clarification – What is 'In-Memory'?**
"In-memory" refers to the complete representation of the document as it exists in the system's temporary working state – fetched either from:
- The full file stored in Git
- Or the active working version stored in a workspace or local document buffer

**Fixes for PolicyGPT:**
1. **Fetch Entire File for Commit:** Always source commit content from the full file in memory or explicitly re-fetch from Git.
2. **Chunk Commit Strategy:** Break very large files into logical sections and commit each part explicitly.
3. **Commit Integrity Checks:** Compare pre-commit and post-commit length or line count to detect truncation.
4. **Canvas Render Limits:** Avoid using canvas-rendered preview for commit operations.

**PolicyGPT Design Implication:**
Ensure that commit actions and review UIs always operate on full-file representations, not UI-limited views.