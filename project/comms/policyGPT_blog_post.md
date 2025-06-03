# Coaching the Machine #5: GovDoc Copilot – Your AI Assistant for Government Project Docs

Welcome to the fifth installment of *Coaching the Machine*, where we continue our experiment in blending human intent with machine execution. This post marks the second deep-dive into a real-world use case—a working proof of concept—and it’s one I’ve built in collaboration with Jesse Moon, a thoughtful technologist with deep roots in the Canadian public sector. Jesse brings over a decade of experience leading strategy and consulting projects across government departments..

This time, we tackled one of the most document-heavy, effort-intensive, and high-stakes environments in the public sector: government project management.

---

## Why Docs Are Prime for AI

When it comes to language tasks, documentation is a goldmine for generative AI—especially large language models (LLMs) like ChatGPT, Claude, Gemini, and others. Think about the workflow:

> **Research → Synthesis → Analysis → Drafting → Editing → Tailoring to Audience → Review → Revision**

That’s the native terrain for LLMs—advanced AI models trained to understand and generate human-like text across many domains and formats. These models have been trained on vast libraries of structured and semi-structured content—think hundreds of thousands of Wikipedia-sized corpora. They understand form, flow, and function.

But there's a catch: on their own, LLMs are not enough.

---

## Why the LLM Alone Falls Short

We’ve all seen the flash of promise followed by the fizzle of failure. On their own, LLMs:

* **Hallucinate:** Confidently make things up.
* **Drift:** Lose the thread across long or complex prompts.
* **Isolate:** Operate outside of the systems we actually use—document stores, reference libraries, APIs.

Worse, the instinct to “just dump everything in” can backfire. A flood of long summaries confuses more than it clarifies. Context matters—but only if it’s clean, structured, and scoped.

*Want to dig deeper? Read more about the risks and real-world consequences of LLM misuse in ********************************************************************************************************************************************************************************[The Guardian’s legal AI mishap](https://www.theguardian.com/us-news/2025/may/31/utah-lawyer-chatgpt-ai-court-brief)********************************************************************************************************************************************************************************, ********************************************************************************************************************************************************************************[The Verge's take on AI hallucinations](https://www.theverge.com/policy/677373/lawyers-chatgpt-hallucinations-ai)********************************************************************************************************************************************************************************, and ********************************************************************************************************************************************************************************[Stanford HAI’s research on legal LLMs](https://hai.stanford.edu/news/ai-trial-legal-models-hallucinate-1-out-6-or-more-benchmarking-queries)********************************************************************************************************************************************************************************.*

---

## The Pattern: LLM + Context + Structure + Integration

Here’s the approach we’ve been refining:

**Four ingredients in a deliberate system:**

1. **LLM** – the brain: powerful, generative, but needs guidance. Think of it like a sharp intern—tools like ChatGPT or Claude can generate, summarize, and respond, but they need direction to stay useful.

2. **Ontology** – the domain: For a PM, this includes how project types, gates, roles, and artifact expectations relate. It helps tailor every step to the right format and context.

3. **Schema & Tools** – the scaffolding: These define the shape of inputs and outputs. For example, a Business Case template with required sections, validation logic, and format.input/output formats, validations, and review cycles.&#x20;

4. **Integration** – how the AI connects to the systems we use every day, so it’s embedded in how work actually gets done. In our PM case, that could mean connecting to document repositories like SharePoint, collaboration tools like Slack, and task management systems like Jira.

Individually, each helps. Together, they unlock exponential value. This is where custom GPTs shine—tuned for specific workflows, speaking the language of the domain, embedded in real processes.

*Curious how this pattern plays out? Check out ********************************************************************************************************************************************************************************[Medium’s intro to Model Context Protocol](https://medium.com/@jai.mail67/solving-llm-integration-challenges-with-model-context-protocol-mcp-and-spring-ai-883a5275b3cb)********************************************************************************************************************************************************************************, ********************************************************************************************************************************************************************************[Wikipedia’s overview of Retrieval-Augmented Generation](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)********************************************************************************************************************************************************************************, or ********************************************************************************************************************************************************************************[Swimm's guide to prompt engineering and context windows](https://swimm.io/learn/large-language-models/llm-context-windows-basics-examples-and-prompting-best-practices)********************************************************************************************************************************************************************************.*

---

## The Use Case: PMs in Government

Managing a project within the public sector is no small feat. Government frameworks — such as the [Government of Canada’s Project Management Framework (PMF)](https://www.canada.ca/en/treasury-board-secretariat/services/information-technology-project-management/project-management/guide-project-gating.html) — involve multiple mandatory documents across various project gates (Gates 0 through 5). These include:

* Business Cases
* Project Charters
* Gating Plans
* Project Management Plans
* Transition and Close-Out Reports

Each artifact has its own structure, approval requirements, and expectations for language and evidence. Producing these documents manually requires not only subject-matter expertise, but also fluency in the framework itself. For overburdened teams, this can delay project startup and drain resources.

> "ChatGPT estimated that across the federal public service, the total time spent producing gated project documentation could easily exceed **1 million hours annually**."
>
> I asked it to estimate based on the number of departments, average number of projects, typical artifact count, and how long these take to draft. Even with conservative assumptions, the effort adds up fast.

**And it’s only getting harder:**

* New mandates every year
* More pressure for innovation and efficiency
* Shrinking teams, tighter timelines

So we asked: **what if AI could take the first swing at this work?**

---

## Meet GovDoc Copilot: PM Edition

To address this, we developed a custom GPT designed specifically for the Government of Canada’s PMF. This AI model understands the structure and intent of each document type and can:

* Draft entire artifacts like Business Cases, Charters, and Transition Plans
* Populate them with accurate, context-specific content based on a few inputs
* Ensure alignment with gating requirements, Government of Canada Mandate Letters, Treasury Board policies, and departmental guidance

For example, the AI can produce a fully structured Business Case that includes:

* A detailed executive summary using the Situation-Complication-Solution format
* Options analysis with risk-benefit comparison tables
* ROI metrics based on reasonable assumptions
* Alignment with GC strategic priorities and funding streams

This is not a simple template filler. The AI captures tone, structure, and contextual alignment — and produces first drafts that are nearly complete, ready for review, refinement, and submission.

---

### ✨ A User Journey: From Concept to Completed Document

We designed GovDoc Copilot around a simple premise: what if a program manager could draft a government business case the way they actually work — and have an AI assistant guide them, step by step?

Here’s what that looks like in action, through a real-world example: preparing a Gate 0 Investment Proposal for a cross-departmental AI Talent Expansion initiative.

#### 🧭 Step-by-Step Journey

**1. Kickoff and Gate 0 Setup**
The user starts with: “*The project is to expand AI talent across departments. We need to prepare for Gate 0.*”
The Copilot responds with a checklist of required artifacts. The user selects: *Investment Proposal Concept*.

**2. Upload Workshop Notes**
The user shares notes: “*See minutes from our brainstorming session.*”
Copilot uploads, summarizes, and indexes them.

**3. Research Alignment**
The user asks: “*What are other jurisdictions doing to support AI talent?*”
Copilot returns examples from the U.S., UK, and EU.
“Record this for the proposal.” It does.

**4. Policy Alignment**
The user asks: “What GoC strategies should we align with?”
Copilot recommends *Canada’s Digital Ambition 2023*, *TBS Directive on Automated Decision-Making*, and *[Prime Minister Mandate Letter 2025](https://www.pm.gc.ca/en/mandate-letters/2025/05/21/mandate-letter)* and extracts key directives.

**5. Review Context Before Drafting**
The user asks for a summary of inputs.
Copilot returns a contextual snapshot: notes, research, and references.

**6. Section-by-Section Drafting**
The user + Copilot drafts sections in turn: Problem Statement,  Outcomes, Benefits, Strategic Alignment.
Each goes through: Copilot drafts → user provides feedback → Copilot revision → user acceptance.

**7. Final QA and Assembly**
The user asks for a final QA. Copilot checks flow and consistency, compiles the document, and outputs the final version.

> This isn’t just a smarter writing tool. It’s a co-pilot that guides process, policy, and product.
>
> * 🧩 Remembers inputs and decisions
> * 📚 Integrates real research and references
> * ✍️ Adapts to tone and structure norms
> * ✅ Runs built-in QA and approval flows
> * 🔁 Supports full iteration, end-to-end

---

### Benefits in Practice

Teams leveraging this AI-assisted approach experience:

* **Accelerated turnaround:** Reduce document creation time from days/weeks to minutes.
* **Improved consistency:** Standardize language, structure, and compliance.
* **Higher confidence:** Reduce rework through clearer alignment with PMF standards.
* **Strategic focus:** Free up staff to focus on planning, engagement, and delivery.

Even for seasoned project officers, the AI becomes a collaborator — suggesting phrasing, surfacing considerations, and pre-populating checklists and schedules.

---

## Under the Hood

Let’s unpack how we built it—without losing our non-technical readers.

### 1. Structured Context, Not a Data Dump

We didn’t just shove documents into the LLM. We:

* Summarized upstream: turned PDFs and URLs into crisp summaries
* Labeled clearly: so the model knows what’s a mandate vs a policy vs a department priority
* Scoped instructions: guiding the model section by section

### 2. Ontology

We produced a detailed map of the Government of Canada’s Project Management Framework, including gates, required artifacts, sections, evaluation criteria, and more ([see link](https://github.com/stewmckendry/ai-delivery-sandbox/blob/sandbox-curious-falcon/project/reference/gate_reference_v2.yaml)). This ontology is what tells GovDoc Copilot how to tailor its research, analysis, drafting, and edits to a specific document. It’s what brings the PMF to life—and it’s easily swappable to support another department’s framework or even a completely different domain (more on that later in the Beyond PM section).

### 3. Toolchain + Orchestration

We wired the system to use the right tool for each step:

* **Copilot Tools:** We built a full suite of modular tools to support the document workflow:

  * `uploadProjectInputs`, `uploadReferenceDocument`, `recordResearchNotes`
  * `generateSectionDraft`, `reviseSectionDraft`, `finalizeArtifact`
  * `submitFeedback`, `reviewInputSnapshot`, `getLatestSection`
  * All of these are swappable, extendable, and composable based on your organization’s needs.

* **Prompt Templates:** for rewrites, executive summaries, citations

* **OpenAPI Schemas:** so the front-end chat can talk to tools like `generateSectionDraft`

The toolchain isn’t hard-coded for government. It’s modular and easily configured for any domain—from policy to procurement to HR.

### 4. Memory Layers

To ensure the Copilot can remember, retrieve, and persist information across sessions, we use a multi-layered memory system:

- **Redis:** Provides fast, short-term memory for tracking draft progress and recent interactions.
- **SQL Database:** Maintains a complete history and audit trail of actions, drafts, and user feedback.
- **Google Drive:** Stores finalized documents for easy collaboration, sharing, and handoff.
- **Chroma Vector Database:** Holds key reference materials (such as policies, strategies, and guidelines) and enables semantic search. This means the Copilot can find relevant content based on meaning, not just keywords—helping answer questions even when phrasing differs.

By combining these layers, the Copilot stays grounded in your context, remembers what’s been produced, and surfaces what matters most at every step.

### 5. Human + GPT + Tools: Division of Responsibility

This is where the real magic happens—a three-way collaboration between the user, the GPT-based assistant, and structured tools behind the scenes. Here’s how the roles break down:

* **You (the user):** You bring situational judgment and real-world priorities—like “we’re preparing for Gate 1” or “use these workshop notes.” You guide the AI on what matters most, and when.
* **The GPT (Copilot):** It brings coherence across inputs, rewrites content on the fly, and maintains a polished, professional voice. It remembers what you’ve told it, and adapts tone, structure, and suggestions in real time.
* **The Tools:** These handle memory, reference integration, formatting, alignment to policy, and output finalization. They make sure everything is traceable, persistent, and consistent across artifacts and revisions.

> On its own, the AI could generate good paragraphs. But with the tools, it becomes a full-stack collaborator. It:
>
> * Keeps context across multiple artifacts and sessions
> * References past research, directives, and your uploaded inputs
> * Guides the entire approval and finalization process

This workflow leverages a proven AI technique called Chain of Thought with ReAct-style reasoning. For each document section:

1. **Draft:** The Copilot generates an initial draft.
2. **Self-Check:** It runs an internal QA to identify issues with tone, flow, or structure.
3. **User Review:** You review the Copilot’s observations and proposed changes.
4. **Revise:** The Copilot updates the draft based on your feedback.

By maintaining context and tracking decisions throughout this loop, the Copilot evolves from a simple responder into a true collaborator—helping ensure clarity, coherence, and compliance at every step.

---

## Built by Pods: AI Agents as Co-Developers

We built this the same way we built the last PoC: with GPT Pods.
Each Pod is a role-specific AI:

* **Product Pod** → scopes features
* **Delivery Lead Pod** → tracks progress
* **QA Pod** → tests drafts
* **Research Pod** → finds patterns and prior art
* **Writer Pod** → creates documentation like this

As a team of one, I worked across all Pods, tasking them in parallel—sometimes 3–4 Pods at once. The hardest part? Avoiding overload or misalignment. Even AI teams need a good delivery manager.

This time, we got better at:

* Splitting work into 30+ features and work packages
* Running structured tests (local → cloud → GPT front-end)
* Iterating faster while keeping everything in Git for traceability

> **What’s next?** Scaling this model to support **multiple people collaborating with multiple Pods**. Instead of teams of 80+, you can imagine 10–15 humans working alongside AI copilots—scoping, building, and shipping together. It’s not just individual productivity—it’s team-scale delivery transformation.

---

## Beyond PM: Where This Pattern Goes Next

This isn’t just for project gates. The same architecture works across domains because it’s powered by modular, swappable components.

**The same ontology approach that powers GovDoc Copilot: PM Edition can be reused across domains.** Since the only PMF-specific piece is [this reference YAML](https://github.com/stewmckendry/ai-delivery-sandbox/blob/sandbox-curious-falcon/project/reference/gate_reference_v2.yaml), it's easy to swap in another department’s framework or a totally different domain—from finance to HR.

So while we call it GovDoc Copilot: PM Edition today… we may need a new name soon.

**📊 Finance:** Annual Reports, Budget Estimates, Financial Variance Reports, Quarterly Results, Grants & Contributions Reports

**📑 Compliance:** Audit Reports, Risk Assessments, Policy Compliance Reviews, Internal Controls Reports, Privacy Impact Assessment, Threat & Risk Assessment

**🧠 Strategy:** Business Plans, Operating Plans, Strategic Frameworks, Environmental Scans, Investment Plans

**👥 HR**: Training & Certification Reports, Recruitment & Hiring Reports, Equity & Diversity Reports, Workplace Investigations

**🚀 Delivery:** Program Evaluations, Project Reviews & Audits, Service Delivery Assessment, Benefits Realization Reports

> Just swap the ontology and tailor the tools, and you’ve got a Copilot for any domain.

---

## 📣 Want to Try or Collaborate?

We’d love your feedback.

📅 Try GovDoc Copilot: PM Edition here: \[Live demo link – insert here when ready]
🎥 Watch a demo video of GovDoc Copilot: PM Edition in action: \[YouTube link – insert here]

📩 Reach us: Stewart ([stewart.mckendry@gmail.com](mailto:stewart.mckendry@gmail.com)) + Jesse ([jdmoon@gmail.com](mailto:jdmoon@gmail.com))
🔍 Want to co-create the next use case? Let’s talk!
