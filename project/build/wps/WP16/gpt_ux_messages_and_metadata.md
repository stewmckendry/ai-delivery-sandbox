# GPT UX Messages, Tool Metadata, and Starter Prompts

## 🎯 Purpose
This file defines the core UX messages and system metadata needed to enable PolicyGPT to guide users through structured or unstructured input collection.

---

## 🧭 GPT Starter Prompts

**Prompt A – Guided Mode (Section by Section)**
> "Would you like to work section-by-section through the required gate documentation? I can guide you and ask only what’s needed."

**Prompt B – Data Dump Mode**
> "Do you have documents or files you’d like me to analyze and extract from to help generate your submission? You can upload them, and I’ll load them into memory."

**Prompt C – Manual Upload + Describe**
> "You can also tell me what kind of document you’re uploading and I’ll log it for future use."

---

## 🛠️ Tool Metadata for GPT Use

### inputPromptGenerator
- **When to Use**: If user agrees to step-by-step guidance
- **Purpose**: Generate structured prompt for the selected gate, artifact, and section
- **Trigger Phrase**: "I want to do guided input" / "Let’s go section by section"

### inputChecker
- **When to Use**: After collecting multiple user responses
- **Purpose**: Validate input completeness against gate_reference
- **Trigger Phrase**: "Have I provided enough?" / "Is this sufficient?"

### loadCorpus
- **When to Use**: When user uploads a document or group of documents for context building
- **Purpose**: Embed and index documents in vector memory for downstream retrieval
- **Trigger Phrase**: "Here are my docs" / "Can you use these to draft the case?"

### uploadTextInput, uploadFileInput, uploadLinkInput
- **When to Use**: Whenever a user provides inputs outside guided flow
- **Purpose**: Log freeform input for memory and future use
- **Trigger Phrase**: "Here’s a summary" / "Let me paste something in"

---

## 💡 GPT Conversation Tips
- Begin by detecting if user prefers guided vs. document-based mode
- Offer both modes upfront
- Use `session_id`, `gate`, and `artifact` metadata tags to keep memory organized

---

## File Owner
WP16Pod
May be referenced by downstream GPT configuration or UX teams.