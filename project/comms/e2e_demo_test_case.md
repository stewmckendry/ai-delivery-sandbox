# E2E Demo Test Case: GovDoc Co-Pilot – PM Edition

## Scenario
You're a project officer in the Canadian government working on a national AI strategy initiative. Your task is to produce a Business Case artifact as part of Gate 1 in the Government of Canada’s Project Management Framework (PMF).

## Objective
Demonstrate end-to-end use of the GovDoc Co-Pilot to generate, refine, and finalize a PMF artifact with minimal input.

---

## Step-by-Step Instructions

### Step 1: Upload Contextual Inputs
**Tool:** `uploadTextInput`

- **Input:**
  ```
  text: "The national AI strategy aims to expand public sector use of artificial intelligence tools for service delivery. The initial scope includes piloting AI assistants in Immigration, Veterans Affairs, and CRA."
  metadata: {
    "project_id": "ai_strategy",
    "session_id": "demo-session-001"
  }
  ```
- **Expected Output:** Success message with file path and metadata confirmation.

### Step 2: Select Artifact Type
**Tool:** `getArtifactRequirements`

- **Input:**
  ```
  project_id: "ai_strategy"
  artifact_type: "Business Case"
  gate_id: "1"
  ```
- **Expected Output:** List of required sections and intents for the Business Case artifact.

### Step 3: Generate Section Drafts
**Tool:** `generateSectionDraft`

- Repeat the following for each section (e.g., `ExecutiveSummary`, `OptionsAnalysis`, etc.)
- **Input:**
  ```
  project_id: "ai_strategy"
  session_id: "demo-session-001"
  artifact_id: "business_case_gate1"
  section_id: "ExecutiveSummary"
  gate_id: "1"
  ```
- **Expected Output:** Markdown draft of the section, incorporating uploaded input, strategic alignment, and research context.

### Step 4: Submit Edits (Optional)
**Tool:** `submitFeedback`

- **Input:**
  ```
  artifact_id: "business_case_gate1"
  section_id: "ExecutiveSummary"
  session_id: "demo-session-001"
  feedback: "Clarify alignment with Treasury Board priorities."
  action: "clarify"
  ```
- **Expected Output:** Updated section draft with improved alignment.

### Step 5: Finalize Artifact
**Tool:** `finalizeArtifact`

- **Input:**
  ```
  project_id: "ai_strategy"
  artifact_id: "business_case_gate1"
  session_id: "demo-session-001"
  gate_id: "1"
  version: "v1.0"
  ```
- **Expected Output:** Google Drive URL with the compiled Business Case, with section titles, formatted content, and citation integrity.

---

## Success Criteria
- Co-Pilot returns usable, well-structured drafts for each section.
- Revisions improve clarity without removing relevant detail.
- Final document is ready for review or submission.

---

## Notes
- Keep browser DevTools open to inspect prompt inputs and outputs.
- You can modify session or artifact ID to test alternate flows.
- Tie-in feedback to strategic documents like Mandate Letters or Digital Ambition 2022.

---

## Sample Inputs for Testing
- **Scope Summary:** "Pilot AI use cases to improve federal service delivery."
- **Stakeholders:** "TBS, SSC, IRCC, CRA, Veterans Affairs."
- **Strategic Alignment:** "Supports GC Digital Ambition, AI Governance Framework, and Ministerial Mandate Letters."

---

## Link to Blog Context
[GovDoc Co-Pilot: PM Edition Blog](https://github.com/stewmckendry/ai-delivery-sandbox/blob/sandbox-curious-falcon/project/comms/govdoc_copilot_blog.md)