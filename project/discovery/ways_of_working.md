### 🧱 Ways of Working – Human + GPT Pod All-Star Team (Updated)

#### 1. **We are a team. We work together.**
We share the mission and move as one.  
**What this looks like:**
- Human Lead sets the goal: *“Let’s do ___ next.”*
- GPT Pod plays back the mission, proposes a plan, and requests any needed inputs (files, assumptions, context).
- Human Lead provides inputs and feedback on the plan.
- GPT Pod locks in v1.0, generates a backlog, and queues up the first step(s).
- Human confirms priority and says *“Patch away!”*
- GPT Pod delivers the patch — code, schema, copy, plan — for approval.
- Human confirms completion or flags issues.
- GPT Pod continues the next batch and keeps us moving.

#### 2. **We iterate quickly.**
Speed is our ally; clarity fuels momentum.  
**What this looks like:**
- Human Lead sets a clear vision and constraints.
- GPT Pod generates 80% drafts with speed and structure.
- Human Lead gives sharp feedback to finalize.
- GPT Pod adapts quickly, increases batch sizes, automates routine.
- We ship an MVP as fast as possible.
- **New:** Tasks are tightly scoped up front using prompt templates and input/output checks.

#### 3. **Git is our source of truth.**
We trust the repo. We sync often.  
**What this looks like:**
- Ask: *“Do we have the latest?”* — always.
- GPT Pod fetches latest files before work.
- GPT Pod searches memory index if unsure.
- Patches apply against latest base.
- Git-native tools (patch, commit, lifecycle) are our norm.
- Task lifecycle is our operating system.
- **New:** GPT Pod warns if overlapping files are in use and verifies commit paths.
- **New:** After each output file is committed, GPT Pod provides a GitHub link to view the file:  
  `https://github.com/stewmckendry/ai-delivery-sandbox/tree/sandbox-silver-tiger/<file_path_from_root_of_branch>`

#### 4. **We document everything.**
If it’s not in the repo, it didn’t happen.  
**What this looks like:**
- GPT Pod commits all outputs to Git.
- Chain-of-thought logs capture task flow.
- Reasoning traces explain how decisions were made.
- Handoff notes guide the next pod (Human or GPT).
- **New:** GPT Pod snapshots decision state and goals before scaling out or completing.
- **New:** GPT Pod logs chain-of-thought for each prompt response to show reasoning and decisions.

#### 5. **We improve the framework.**
This project makes the ai-delivery-framework better.  
**What this looks like:**
- Log every issue — bugs, gaps, feature ideas.
- If blocked, escalate to the framework support pod.
- Experiment, observe, and reflect.
- **New:** Learnings from each task are summarized and proactively surfaced.

#### 6. **We take a full-stack, multi-lens view.**
We think in systems, not silos.  
**What this looks like:**
- Discovery explores users, tech, data, workflows, and edge cases.
- Solution design spans client, backend, model, and cloud.
- We don’t just ship code; we ship understanding.
- **New:** Every phase includes a UX and persona usability lens.
- **New:** GPT Pods and Human Lead align early on data schemas with sample data to ensure front-end and back-end coordination.

#### 7. **We build something awesome users love.**
If it’s not useful or delightful, it’s not done.  
**What this looks like:**
- Users are part of every phase — not an afterthought.
- We ask: *“Would this be better than just using ChatGPT?”*
- We care about flow, clarity, and impact.
- **New:** Outputs are reviewed for clarity and usability before approval.

#### 8. **We relate it to Coaching the Machine.**
This is a teaching moment for teams and youth.  
**What this looks like:**
- Use sports metaphors to explain delivery patterns.
- Reflect on what this teaches us about leading, teaming, and training AI.
- Make it personal, engaging, and real.

#### 9. **We keep context clean.**
Context creep causes confusion.  
**What this looks like:**
- We scale out to new pods when threads get too long.
- GPT Pod resets assumptions instead of guessing.
- **New:** GPT Pod saves periodic context snapshots and tracks branch safely.

#### 10. **We close the loop.**
Finishing strong means reflecting and learning.  
**What this looks like:**
- Every task ends with a reasoning trace and next-step plan.
- Learnings are logged to improve future work.
- **New:** GPT Pod offers post-completion metadata updates and traces for reflection.

---

### 📂 Folder Structure for Project Work
All active work takes place under `/project/`. The `/framework/` folder is read-only reference. Pods should use the following structure:

```
/project/
  discovery/
    users/               # personas, interviews, user journeys
    market/              # comps, trends, inspiration
    scope/               # goals, flows, requirements
  development/
    prompts/             # task prompts, prompt templates
    features/            # feature folders, each with code + tests
    data/                # grounding, sample data, pipelines
  testing/
    qa/                  # test cases, test plans
    results/             # test run outputs, bugs
  go-live/
    deployment/          # deploy guides, checklists
    feedback/            # launch feedback, user reports
    metrics/             # success metrics, tracking setup
```