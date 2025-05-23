# 🧩 WP17b Note – Prompt-Level Chunking for Token Management

## 🎯 What It Is
Prompt-level chunking is the process of splitting long inputs (or outputs) into smaller pieces **before** sending them to GPT — specifically to manage token limits.

This differs from `draft_chunks` (used in `ReasoningTrace`) which are about traceability, not runtime limits.

---

## 🚫 Current State
- We **do not** currently chunk prompts or responses for token reasons.
- Tools assume the full prompt or memory fits within one GPT call.
- `draft_chunks` (in ReasoningTrace) are created *after* the full draft is generated, and help with versioning and display.

---

## 🧠 Why It Matters
- GPT-4-turbo supports up to 128k tokens, but actual limits vary with deployment and cost.
- As `memory` grows (via PromptLog or embeddings), prompt sizes will easily exceed token budgets.
- Long sections or template-driven generation could require multi-pass streaming or batching.

---

## 🔧 What to Build
A utility function or class such as:
```python
from tiktoken import encoding_for_model

def tokenize_and_chunk(text: str, max_tokens: int = 300):
    """Split text into token-aware chunks"""
    ...
```

Then update tools like `section_synthesizer` to optionally:
- Chunk the context (e.g., `memory`)
- Generate a draft per chunk
- Stitch drafts back together

---

## 🔄 Interaction with Trace Chunking
| Feature            | Prompt Chunking         | Trace Chunking          |
|-------------------|-------------------------|--------------------------|
| When it occurs    | Before GPT call         | After GPT call           |
| Purpose           | Token limits            | Traceability, diff, UX   |
| Structure         | Internal to tool prompt | Stored in ReasoningTrace |

### Learnings to Reuse
- Same paragraph split logic (if used)
- Chunk structure could evolve to share fields (e.g., `chunk_id`, `position`)

---

## 📚 Impact Assessment
- No DB schema change needed
- Tool wrappers may need to:
  - Loop over chunks
  - Combine partial outputs
  - Modify how `prompt_used` is logged

## 🗂️ Reference Files
- `section_synthesizer.py`
- `section_refiner.py`
- `section_draft_output.py`
- `memory_retrieve.py` (if chunking memory)
- `draft_chunks` field in `ReasoningTrace`

---

## 📝 Suggested WP Scope
"Implement token-aware prompt chunking logic and integrate into at least one GPT tool (e.g., section_synthesizer). Ensure trace and section output match prior behavior."

- Write token-aware chunking util
- Patch tool wrapper
- Retain compatibility with ReasoningTrace format
- Add CLI test for large memory context