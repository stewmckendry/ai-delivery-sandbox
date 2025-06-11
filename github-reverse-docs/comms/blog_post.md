# Modernizing Legacy Systems with AI: What’s Now Possible

AI agents are getting more connected to your data & tools. Can they now close knowledge gaps in legacy systems and support faster, safer modernization?

---

Welcome to the sixth post in **Coaching the Machine**, where we explore how humans and AI can build together.

In recent editions, we showcased greenfield PoCs:

- **Delivery Pods** – AI copilots that help teams build and ship software
- **ConcussionGPT** – a homegrown AI agent for concussion triage and return-to-play
- **GovDoc Copilot** – an AI assistant that helps draft complex government documents like business cases and project plans

These examples were powerful because they showed what AI can do when it’s building something new—with a clean slate.

But what about the messy stuff?

---

## The Legacy Challenge

Every IT leader knows the real pain lies not in starting fresh—but in dealing with what already exists:

- Legacy systems built over years
- Incomplete or outdated documentation
- Key people who’ve moved on
- Code that still “works,” but no one fully understands

Before you can modernize, migrate, or onboard a new team, you need to understand what you’re working with. That typically means a costly, time-consuming current state assessment—pouring over code, tracing dependencies, and trying to reverse-engineer tribal knowledge. And even then, blind spots remain. It’s risk mitigation, not acceleration.

---

## Why This Matters Now

With ChatGPT’s newest features—**Deep Research** and the **Codex agent**, both now connected to your live GitHub repos—we saw an opportunity:

> Could an AI assistant help make sense of legacy codebases faster? Could it generate usable documentation, uncover system structure, and reduce the unknowns that stall modernization?

In other words: **Before we ask AI to build something new, can it first help us understand what we already have?**

To find out, we pointed both features at our own system—GovDoc Copilot—and asked them to explore, explain, and document what they found.

Here’s what we learned.

---

## The New ChatGPT Features We Put to Work

### 1. Deep Research + GitHub Connector

OpenAI recently launched data connectors in ChatGPT, allowing it to connect directly to tools like GitHub, Google Drive, and more. One mode—**Deep Research**—lets GPT read deeply across many files and generate rich, synthesized insights.

In past PoCs like GovDoc Copilot (Blog 5), we built our own integrations to feed ChatGPT the data it needed—from Google Drive to Redis to internal databases. That worked, but it required plumbing.

Now, this kind of integration comes out-of-the-box. With just a few clicks, GPT can see the real files your team uses every day—no manual uploads, no workarounds.

**Why it matters:**

- No need to upload files manually
- GPT can read and reason over your actual systems and codebases
- Honors your security settings; only accesses what you grant
- A step closer to AI as a context-aware assistant embedded in your workflow

For teams working on complex or legacy systems, this opens the door to something new: automated analysis of code and documentation, from within the real working environment.

To test this, we wired ChatGPT to our GitHub repo for GovDoc Copilot—the same project from the last blog—and gave it no prior context. The challenge: could ChatGPT learn the system from scratch, and generate useful and accurate documentation?

If this works, it could change how teams onboard to legacy systems, prepare for modernization, or reduce risk before touching a line of code. Instead of weeks or months of ramp-up, could a new developer or analyst hit the ground running in hours?

We ran 5 iterations, each refining the prompt based on the last output. It generated user stories, design artifacts, test plans, and modernization opportunities.

- [Deep Research prompts, outputs, and evaluations here →](#)
- [Final report output →](#)

---

### 2. Codex + GitHub

OpenAI’s **Codex agent** is also back in a new form—now wired to GitHub and optimized for reasoning over codebases. Unlike traditional autocomplete tools, Codex can execute multi-step tasks inside an isolated sandbox. You can ask it to:

- “Explain a repo to a new developer”
- “Find and fix bugs”
- “Propose enhancements”
- “Generate code, tests, or refactors, and create a PR”

It doesn’t just summarize—it codes. In our test, Codex generated working code patches and opened a pull request to merge to the Git repo, all from inside ChatGPT.

Codex runs tasks in an isolated cloud sandbox with no internet access. It can run tests, apply linters, and commit changes for review—but it can’t install new system packages or access private dependencies unless they’re already available in the sandbox.

We ran Codex against the same repo and asked it to generate the same four types of documentation. Its output was leaner, more technically precise, and schema-aware.

- [Codex + Git test session →](#)

---

## Comparing the Outputs

Each tool brings a different strength to the table:

- **Codex** is your precision engine. It reads code directly, identifies structure, surfaces components and interfaces, and can generate working code or pull requests. It’s ideal for quickly understanding the *how* of a system: its data flows, schemas, and logic.
- **Deep Research** is your synthesizer. It turns raw facts into narratives and insights—generating user stories, modernization opportunities, and documentation that connects technical components to business purpose. It also pulls in adjacent context from files, logs, reports, or connected tools like SharePoint and Teams.

**When used together:**

1. Run Codex first to get the architecture, components, and ground truth right.
2. Then use Deep Research to build documentation, explain usage patterns, and identify modernization angles.

This pairing accelerates:

- Developer and vendor onboarding
- Current state understanding
- Project documentation and planning
- Early risk identification before modernization begins

**Bottom line:** Codex gives you code confidence. Deep Research gives you context. Together, they close critical gaps in legacy system understanding—before you rebuild or replace anything.

---

## Artifacts AI Generated to Understand the Legacy System

Here are real examples of what Deep Research and Codex produced when analyzing our codebase—ranging from user stories and technical designs to test outlines and modernization ideas. These aren’t samples—they’re grounded, relevant, and useful.

### 🧑‍💼 User Story

> As a project stakeholder, I want to provide project details (text, file, or link) and have the system create a structured Project Profile, so that all key project information is captured for reuse.

**Acceptance Criteria:**

- Given a valid input, the system generates a profile with fields like project_id, title, and scope_summary
- If a profile already exists, the system merges new data (preserving existing values where applicable)
- A last_updated timestamp is added
- Data is saved using the ProjectProfileEngine and stored via SQLAlchemy models

*Assumptions:* OpenAI GPT-4 is used to parse raw inputs into structured fields; required fields (e.g. project_id) must be present or an error is raised.

---

### 🧩 System Design (Excerpt)

The system is structured into modular toolchains managed by a central Planner/Orchestrator, which maps high-level intents (like "generate_section") to predefined workflows.

- **PlannerOrchestrator:** Dispatches the appropriate toolchain class based on intent.
- **IngestInputChain:** Ingests and parses raw inputs into structured project profiles.
- **GenerateSectionChain:** Composes a section by retrieving memory, generating content with citations, and refining output.
- **AssembleArtifactChain:** Gathers and formats all sections into a complete document.
- **ReviseSectionChain:** Applies user feedback to update drafts, versioning the changes.

Each chain logs intermediate results, saves outputs to the database, and supports extensibility through a common interface (`run(inputs)`).

---

### 🧪 Testing Focus Areas

- **Content Quality:** Feed a bullet list to generate_section_chain and verify coherent, well-formatted output.
- **Chunking & Limits:** Confirm behavior with large inputs—should handle token limits gracefully.
- **Revision Handling:** Inject feedback like “expand on risks” and check that the section_refiner integrates it correctly.
- **Versioning:** Ensure all sections saved include version tags and that assembly uses the latest approved version.
- **Edge Cases:** Handle misaligned inputs (e.g., unexpected sections or gates), and ensure graceful planner fallback.

---

### 🛠️ Modernization Opportunities

- **Export Flexibility:** Add destinations like SharePoint or OneDrive by abstracting storage.
- **Collaborative Editing:** Use Google Docs API to allow in-place edits before upload.
- **Auto-formatting:** Normalize fonts and apply section templates before export.
- **Notifications & Webhooks:** Email or Slack notifications when docs are ready; callback endpoints for approvals.

**Performance Optimization:**

- Replace flat logs with vector databases (e.g. FAISS, Pinecone) for semantic memory
- Cache repeated LLM calls where inputs haven’t changed
- Run steps like drafting and web searches concurrently with async execution to improve throughput

---

## Reflections: How It Scales

Our GovDoc Copilot repo had ~150 files. Deep Research scanned about half in a single session—which is promising. But most enterprise systems are much larger, often spanning thousands of files and services.

Neither Deep Research nor Codex processes full repositories end-to-end in one go.

- Deep Research supports up to ~192k tokens of context per task (enough for several dozen files).
- Codex works in a secure sandbox and has more limited visibility—what it can access depends on which files are indexed and available to the agent.

For larger systems, you’ll need to break the analysis into manageable slices. You can:

- Divide the repo by domain, service, or directory
- Run targeted AI sessions focused on specific features or workflows
- Chain prompts over time to build a full system map and documentation set

The goal isn’t a single perfect output. It’s a faster, smarter path to baseline understanding—surfacing key components, dependencies, and modernization priorities long before a human team could.

---

## Business Value

Done well, this approach can support:

- Faster onboarding for new team members, vendors, or partners
- Lower cost and risk during discovery and modernization planning
- Clearer documentation to support compliance and project handoffs
- Better decision-making with fewer blind spots

---

## What’s Next

This PoC focused on reverse engineering a legacy system—but the same approach could support many use cases across public sector teams:

- **Business analysis:** Understand how systems align with policies, mandates, or service needs
- **Code reviews:** Identify security, compliance, or usability issues
- **Onboarding:** Generate high-quality docs for new developers or vendors

And this is just GitHub.

ChatGPT now supports other connectors too:

- **Google Drive:** Extract insights from shared folders for onboarding, training, or research
- **SharePoint:** Summarize wikis and docs for live Q&A or artifact generation
- **Custom connectors (Pro/Enterprise):** Securely link internal PDFs, dashboards, or systems using model context protocol (MCP)

---

## What You’ll Need

To try these features:

- **ChatGPT Plus** includes limited access to Deep Research (10 full + 15 lightweight tasks/month)
- **ChatGPT Pro or Enterprise** unlocks higher limits and access to Codex
- Codex currently runs only in ChatGPT UI, not in IDEs (unlike Copilot)

---

## Related Tools to Watch

Most AI developer tools today are focused on helping engineers write, refactor, or autocomplete code—useful, but narrow in scope.

This experiment explored something different: **Can AI act as a system-level analyst**—surfacing architecture, workflows, gaps, and modernization opportunities across a legacy codebase with little or no human context?

That opens up new possibilities for onboarding, modernization, compliance, and risk reduction—especially in environments where documentation is scarce and system knowledge has walked out the door.

A few other tools are evolving in this direction or support adjacent use cases:

- **GitHub Copilot Enterprise** – In-IDE autocomplete with context from your repos and wikis; fast and smart, but not autonomous
- **Anthropic Claude (Code/Opus)** – Strong reasoning and refactoring for complex logic and code reviews
- **Google Gemini Code Assist** – Competes with Codex for multi-file generation and repo understanding
- **Cursor** – An AI-native IDE optimized for reading, editing, and refactoring large codebases in real-time
- **Amazon Q Developer** – AWS-native coding assistant, strong for secure, cloud-integrated workflows
- **Lutra.AI** – General-purpose productivity assistant that connects apps like Slack, Drive, Jira, and Notion for search, Q&A, and automation

Expect this space to evolve rapidly. As AI agents gain access to more of your systems, they’ll play a bigger role in understanding, maintaining, and modernizing the infrastructure that runs your organization.

---

## 📣 Want to Try This or Collaborate?

I’d love your feedback—and I’m always looking for others who want to push the edges of what’s possible with AI + systems work.

- 🧾 **Final Report (Deep Research):** View the full reverse-engineering report on GitHub — includes all prompts, outputs, and evaluations
- 💻 **Codex + Git Test Session:** See the Copilot in action — explore how Codex generated and proposed real code changes
- 📬 **Reach Me:** Stewart McKendry — [stewart.mckendry@gmail.com](mailto:stewart.mckendry@gmail.com)
- 🤝 **Want to co-create the next use case?** Let’s talk—whether it’s greenfield builds, legacy modernization, or helping teams onboard faster with AI copilots.
