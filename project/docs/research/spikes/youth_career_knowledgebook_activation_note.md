**Subject:** Research Spike Activation – Youth Career Knowledgebook for GPT Coach

Hi ResearchPod 👋

You're on deck for task **`1.5_research_spikes`** in the `ai-delivery-sandbox` repo on branch `sandbox-silent-otter`.

---

### 🧠 Your Mission:
Research and compile a rich, age-appropriate **career knowledgebase** to power our **GPT Youth Career Coach** using RAG. We’re aiming for content that’s inspiring, diverse, and written for kids and teens exploring their futures.

---

### 🎯 Your Deliverables:
1. **Markdown summary of key insights, patterns, themes**  
   📄 Path: `/project/docs/research/spikes/youth_career_knowledgebook.md`

2. **Structured YAML grounding file**  
   📄 Path: `/project/inputs/knowledgebooks/youth_career_guide.yaml`

The YAML should include:
- Career titles + fun metaphors (e.g., “The Storyteller of Systems”)
- Core skills, values, or traits per career
- Optional inspiration quotes, examples, or recommended learning paths

---

### 📂 To Get Up to Speed:
Please review the following foundational files:
- `/project/docs/project_goals.md`
- `/project/docs/users_and_journeys.md`
- `/project/docs/features/feature_list.md`
- `/project/docs/features/acceptance_criteria.md`
- `/project/docs/ways_of_working.md` ✅

These explain what we’re building, for whom, and how we work as a Human + AI team.

---

### 🛠️ Tool Calls You’ll Use:
1. **Fetch Files:**  
   Use `fetchFiles` (mode=`batch`) to pull all reference docs.

2. **Log Chain of Thought:**  
   Use `manageChainOfThought` to track your research journey.

3. **Commit Outputs:**  
   Use `commitAndLogOutput` or complete the task using `manageTaskLifecycle`.

4. **Submit Reasoning Trace:**  
   Complete the task with a reflection on sources, synthesis, and opportunities for the coach.

---

Thank you for coaching the machine.  
Let us know if you need help — PromptPod and the Human Lead are here to jam with you anytime.