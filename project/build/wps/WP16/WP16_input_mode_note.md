### 🧭 WP16 Input Mode Note – Guided vs. Data Dump

This note documents the handling of the two input modes (guided and data dump) for the PolicyGPT Input UX Layer, given the constraints of the OpenAI Custom GPT chat interface.

---

### 🎛 No Native UI Toggle Available

Because PolicyGPT runs within the OpenAI Custom GPT environment, there is **no native UI toggle, radio button, or setup wizard** to capture mode preference. Instead, all interactions occur through the chat interface.

---

### ✅ Proposed Mode Selection Flow

1. **System Prompt and Conversation Starters**:
   - The system prompt will **describe the two modes** and GPT’s expected behavior in each.
   - Conversation starters (customizable in ChatGPT) will include options like:
     - “Walk me through building a Gate 0 document step-by-step” (guided)
     - “I’ll upload all my files for Gate 0” (data dump)

2. **Mode Recognition**:
   - Based on user input, GPT determines the mode and stores it in session metadata.
   - Guided mode → invokes tools like `inputPromptGenerator`
   - Data dump → prompts user to upload files, which go through the WP9 upload tools

3. **Session Memory**:
   - A `mode` field (guided | bulk) is tracked in memory or session snapshot for downstream use.

---

### 🛠 WP16 Responsibilities

- Document mode options and behavior
- Implement mode-aware UX flow using conversation and tool calls
- Provide a system prompt template for guided vs. bulk mode
- Recommend session metadata structure (e.g. `{ mode: "guided" }`)

---

### 🔜 Future Tasks

- **Update Custom GPT Config (system prompt + starters)** → Post-WP16
- **Validate mode tracking in session memory** → In collaboration with Memory/Infra pods

This approach ensures a clear, mode-aware interaction flow without relying on UI elements not supported in OpenAI's native GPT chat product.