**Subject:** Architecture Task Activation – Define System for GPT Youth Career Coach

Hi ProductPod 👋

You're now picking up **Task 1.6_define_architecture** in the `ai-delivery-sandbox` repo on branch `sandbox-silent-otter`.

---

### 🎯 Your Mission:
Design the system architecture for the **AI Career Coach app** — powered by GPT, RAG, and optional backend memory.

Your outputs should include:
- A system diagram (frontend + GPT + YAML-based RAG + backend optional memory)
- Description of the data flow across components
- Highlight any assumptions or risks

---

### 📂 Files to Review First:
- `project/docs/project_goals.md`
- `project/docs/users_and_journeys.md`
- `project/docs/features/feature_list.md`
- `project/docs/features/acceptance_criteria.md`
- `project/docs/research/spikes/youth_career_knowledgebook.md`
- `project/docs/research/spikes/youth_career_knowledgebook_handoff_summary.md`

---

### ⚙️ Architectural Requirements:
Your system design should support:
- **Prompt Selector UI** and **Guided Q&A Flow**
- GPT integration with structured, friendly coaching prompts
- RAG: load one or more YAML career segments for grounding
- Optionally persist user reflections (Airtable, Notion, etc.)
- Segment careers by category (STEM, Creatives, etc.)

---

### 🛠 How to Work:
- Commit all diagrams + descriptions to Git
- Use `manageChainOfThought` to log reasoning
- Complete the task with `manageTaskLifecycle` and include reasoning trace
- Visuals are encouraged!

Excited to see how you bring this vision to life! Feel free to ping PromptPod or the Human Lead if you need support.