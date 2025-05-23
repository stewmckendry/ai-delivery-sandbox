## GPT Review Interface Spec (WP16)

### Overview
This interface enables users to review their submitted inputs and confirm readiness to generate a draft artifact. It is designed for a seamless end-to-end experience within PolicyGPT, integrating structured input prompts, input checking, and memory logging.

### User Journey Pathways

#### Pathway 1: Guided Input Collection
1. User initiates artifact creation by selecting gate and artifact.
2. Tool: `inputPromptGenerator` builds section-by-section structured questions.
3. User responds to each question.
4. Tool: `inputChecker` validates completeness vs. `gate_reference_v2.yaml`.
5. Interface shows summary of user responses.
6. User confirms to proceed to draft.

#### Pathway 2: Data Dump Upload
1. User uploads files, links, or bulk text.
2. Tools: `uploadTextInput`, `uploadFileInput`, `uploadLinkInput`, `loadCorpus` extract and log input with metadata.
3. Interface summarizes uploaded content by gate/artifact/section.
4. User confirms to proceed to draft.

### Tools & Components
- `inputPromptGenerator`: Generates input questions per section/intent.
- `inputChecker`: Assesses completeness.
- `PromptLog`: Stores all inputs with metadata.
- `loadCorpus`: Stores bulk references to vector DB.
- `createSessionSnapshot`: (optional) captures full history.

### Custom GPT Configuration
**Name**: PolicyGPT (Draft Assistant)  
**Description**: Supports government project teams in preparing policy artifacts through guided inputs, validation, and draft generation.  
**System Prompt (Instructions)**: You are PolicyGPT, a documentation assistant helping teams prepare for decision gates. Use structured prompts to collect key inputs, validate them for completeness, and generate clear, policy-aligned drafts. You understand gate metadata and ask clarifying questions if data is vague or incomplete.  
**Conversation Starters**:
- "Help me write an Investment Proposal."
- "Can I upload my project documents?"
- "Am I missing anything before I draft?"
- "What does Gate 1 require?"
- "Summarize the key inputs for this section."

**Tool API Setup**:
Tools to include in manifest:
- `inputPromptGenerator`
- `inputChecker`
- `uploadTextInput`
- `uploadFileInput`
- `uploadLinkInput`
- `loadCorpus`
- (future: `queryCorpus`, `compose_and_cite`, etc.)