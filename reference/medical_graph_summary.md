# Concussion GPT Medical Knowledge Graph Summary

## 1. Overview: Knowledge Graph and Its Role

This medical knowledge graph serves as the structured foundation for concussion assessment, tracking, and recovery guidance within the Concussion GPT app. It codifies clinical concepts into machine-readable formats that support:

- Triage and symptom interpretation
- Stage-based recovery planning
- Red flag detection and risk routing
- Integration with clinical guidelines (e.g., SCAT6)
- Preparation for downstream EHR export (e.g., FHIR)

Importantly, this structure is used **as clinical guidance, not rigid output**. The GPT agent is designed to use this content to:
- Anchor semantic interpretation (e.g., symptom severity, duration)
- Offer medically accurate and personalized responses
- Preserve clinical integrity while enabling fluid, natural conversations

Think of the GPT as a "clinically fluent assistant" — combining evidence-backed guidance with contextual awareness and soft-touch dialogue.

## 2. YAML Reference Files and Schemas

### 🔷 `stages.yaml`
**Path:** `reference/stages.yaml`
Describes structured stages of concussion recovery.

**Schema:**
- `id`, `stage_number`, `name`, `description`
- `allowed_activities`, `contraindicated_examples`
- `progression_criteria`, `stage_criteria_logic`
- `duration_guidance`, `guidance_phrases`
- `tool_tags`

**Use:** Determines what stage a user is in, flags risks, guides safe progression.

### 🔷 `symptoms_*.yaml`
Five domain-specific files:
- `reference/symptoms_physical.yaml`
- `reference/symptoms_cognitive.yaml`
- `reference/symptoms_emotional.yaml`
- `reference/symptoms_sleep.yaml`
- `reference/symptoms_red_flag.yaml`

**Schema:**
- `id`, `name`, `category`, `description`
- `severity`, `risk_level`, `onset_timing`, `typical_duration`
- `aliases`, `keywords`, `example_user_utterances`
- `flags` (structured with `type`, `condition`, `advice`)
- `guidance`, `tool_tags`

**Use:**
- Extract and interpret symptoms from user input
- Trigger red flag alerts
- Support follow-up and recovery tracking

### 🔷 `triage_map.yaml`
**Path:** `reference/triage_map.yaml`
Defines conversational stages and diagnostic questions.

**Schema:**
- `triage_flow` → list of `stages`
- Each `stage` includes `id`, `name`, `questions`
- Each `question` includes:
  - `id`, `prompt`, `type`, `intent`, `mode`
  - `response_parsing`, `example_user_answers`
  - Optional: `symptom_links`, `red_flag_check`, `followup_conditions`, `tool_tags`

**Use:**
- Drives symptom intake
- Detects risk and escalation scenarios
- Populates structured logs for review and EHR export

## 3. Application Integration and Flow

### 🔁 Process Flow
Aligned with discovery flows, the app will:
1. Start with a symptom intake or incident report
2. Ask clarifying triage questions
3. Identify symptoms and red flags
4. Track recovery and recommend safe progression stages
5. Provide structured outputs to feed tools and clinicians

### 🧩 Implementation Guidance
- Each response is stored using its `id`, enabling structured memory and tracking
- `response_parsing` and `parse_with` guide how to extract usable data
- Symptom and stage decisions are inferred from the graph, not hard-coded
- Red flags trigger escalation via `tool_tags`
- Supports natural, nonlinear conversation

### 💬 Answers to Integration Questions
> Is the triage_flow order guidance or restrictive?

**Guidance.** The user may answer questions out of order. The app infers answers using symptom mapping, keyword detection, and memory.

> Will GPT know how to parse user answers?

Yes. Fields like `response_parsing` (e.g., "yes/no", "text", "list of symptoms") and tools like `symptom_extractor` guide GPT’s interpretation.

> Will user answers be stored?

Yes. Responses are logged against question `id`s for context reuse, follow-up logic, red flag detection, and EHR integration.

> How will the app decide if there's a concussion?

It combines:
- User symptoms (linked in `symptom_links`)
- Red flag triggers (`tool_tags`, `red_flag_check`)
- Confirmed diagnosis (`diagnosed_concussion`)
- Symptom patterns and progression over time

Final determination requires clinical review, but GPT and tools can surface likely scenarios and urgency.

## 4. Research Sources

- **SCAT6 (BJSM 2023)** – Return to play protocol and symptom taxonomy
- **CDC HEADS UP** – Pediatric symptom guidance and red flag criteria
- **Pediatrics / BJSM / AAN** – Peer-reviewed literature on concussion evaluation and recovery
- **Previous YAML drafts** – Adapted and upgraded from prior project files