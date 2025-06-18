MyHealth Copilot: Reclaiming Your Health Data with AI
By Stewart McKendry, Will Falk, and Jocelyne Verity

Welcome to the seventh post in Coaching the Machine, where we explore how humans and AI can build together.

This one’s a collaboration with two exceptional minds in healthcare: Will Falk and Jocelyne Verity. Both are seasoned healthcare executives, policy leaders, and champions for system transformation in Canada. This post wouldn’t exist without their curiosity, feedback, and encouragement.

✨ What If You Had a Personal Health Concierge?
"I needed my MRI report... but it was locked in one hospital portal. My bloodwork was somewhere else. I had no idea what any of it meant."

Sound familiar? For most Canadians, this is a typical experience.

Health data exists. Access technically exists. But it’s fragmented, scattered across portals, buried in PDFs, and loaded with jargon.

This is where our latest project, MyHealth Copilot, comes in.

It’s a secure digital assistant that helps you:

Log in and retrieve your health information

Understand it in plain language

Use it to support your care journey

Instead of waiting for every system to connect through centralized platforms, the Copilot flips the model:

The patient becomes the integration point.

Importantly, MyHealth Copilot is not a replacement for the many dedicated efforts in digital health across Canada. From national standards through Canada Health Infoway, to provincial platforms like Alberta’s Connect Care or Ontario’s Health Gateway, and even local EMRs and lab portals—progress is real. This tool is meant to complement those systems: a patient-facing bridge that works with what exists today, not against it.

🚀 From Talk to Action: Meet OpenAI Operator
In Blog 6, we explored OpenAI’s Data Connectors and tested them on a real GitHub repo. That’s one path to integration: get API access to source systems, then let AI agents read and reason through structured data.

But here’s the catch: most healthcare providers don’t expose APIs to the public. And for good reasons:

Privacy and security risks

Regulatory constraints (PHIPA, HIPAA)

Complexity of legacy systems

Instead, patients are given access through portals—online dashboards like:

MyChart (used by Ontario hospitals like Unity Health, UHN)

LifeLabs and Dynacare for lab results

Shoppers Drug Mart or Rexall for prescriptions

Provincial vaccine systems (e.g., Ontario Health Gateway)

These portals are secure—but siloed. And patients are often left navigating them alone.

This is where Operator shines.

Operator is part of the shift toward agentic AI — AIs that don’t just talk, but do.

Sam Altman calls it a move toward the "super assistant," handling routine browser tasks so humans can focus on higher-level work.

Operator is an AI agent that uses a real browser—just like a human would. It clicks, types, scrolls, downloads—just like you. But it only acts with your permission. And it pauses at sensitive steps like login.

It’s not scraping. It’s not bypassing rules. It’s working transparently, with you.

Other Operator use cases include:

Booking flights and hotels

Reordering Uber Eats or Instacart groceries

Filling out tax or insurance forms

In our case? It logged into hospital and lab portals, found visit notes and test results, and downloaded them as PDFs and HTML—with the user consenting, watching, guiding, and approving each step.

📂 How It Works
Here’s what it looked like in our real-world test:

A user chatted with the Copilot and said, “Help me collect my recent health records.”

The Copilot launched Operator with a clear task: locate lab results, visit summaries, and recent activity data.

The user manually logged into three different portals—a fitness app, a lab provider, and a hospital record system.

Operator guided the session step by step:

It paused at each login screen, letting the user take over.

It resumed after login to navigate menus and pages.

It displayed everything it was doing (like clicking, scrolling, downloading).

The user could interrupt or override at any time.

Once files were downloaded (as PDFs and HTML), the Copilot prompted the user to upload them securely via a time-limited link.

On upload, the backend extracted and structured the data—labs, visit notes, and summaries—just for that session.

The user could then ask questions like:

“What do these lab results mean?”

“Why did I visit the ER in February?”

“Has my activity improved since last fall?”

The Copilot responded with grounded answers and generated a downloadable summary PDF for personal or clinical use.

All of this happened with real data, real systems, and full user control—proving that AI-assisted health data navigation is no longer theoretical. It’s already happening.

🌍 Who This Helps
Patients want more access, clarity, and control.

This tool helps them gather their records from multiple portals.

It explains medical jargon in plain language, and in their preferred language or style, to match health literacy needs.

It helps guide them through next steps, especially for low-risk or routine items that don’t require clinical intervention.

It empowers them to take more ownership over their care journey—and boosts health literacy in the process.

Most importantly, it helps them feel prepared and informed for appointments.

Clinicians may ask: Can I trust this info? Is it up to date?

That’s valid. The Copilot doesn’t create or modify records—it simply helps the patient retrieve what exists and ask better questions.

Clinicians can view summaries as patient-provided context—not a replacement, but a starting point.

Over time, tools like this could reduce miscommunication, flag inconsistencies, and even surface missing follow-ups.

Administrators & Policymakers are navigating workforce shortages, budget pressures, and rising expectations.

This model offers a new way to extend capacity: let AI handle rote tasks like login, navigation, summarization.

It can reduce support tickets ("I can’t find my test results") and empower patients to help themselves.

Continuity improves when patients carry a complete, portable history across providers.

And perhaps most importantly—it enables improvement without waiting for a full system overhaul.

🔐 People, Privacy & Compliance: Strengths and Gaps
We designed this system to be safe-by-default, but no solution is perfect—and trust depends on transparency.

Here’s our current stance across the three pillars of responsible adoption:

🧑 People
The user remains in control at every step: login, review, upload.

Copilot explains what’s happening, and Operator prompts for confirmation before any action.

But there’s still a digital divide: not everyone has the skills or confidence to guide an AI browser or interpret health summaries.

Where we’re strong: Human-in-the-loop design that’s clear and consent-driven.
Still needed: Digital literacy support, caregiver delegation features, and broader testing across age, ability, and access.

🔐 Privacy & Security
No credentials are stored; Operator pauses at login and uses screenshots.

Files are uploaded to secure storage with short expiration windows.

Nothing is used for model training or shared beyond the user.

Where we’re strong: Encryption, session-level storage, opt-in processing.
Still needed: Clearer consent dialogs, explicit deletion controls, and third-party security audits.

⚖️ Legal & Compliance
The model avoids backend API access and processes only user-directed uploads.

Our architecture aligns with PHIPA principles (Canada) and HIPAA intentions (U.S.), but we have not signed a formal HIPAA BAA with OpenAI.

Terms of Service vary: some portals tolerate assisted access if the user stays in control; others prohibit all automation.

Where we’re strong: Transparent data flows, manual approvals, sandboxed files.
Still needed: Formal privacy reviews, clearer terms navigation, and work with providers to pilot compliant models.

We see this as a step forward—not a solved problem. Our goal is to enable safe innovation and create space for deeper dialogue around what ethical AI in health should look like.

⚠️ Operator Is Still in Preview
While Operator worked effectively in our tests, it remains in technical preview and has some known limitations:

❌ Some sites block or challenge Operator with Cloudflare or CAPTCHA protections

❌ It’s not yet fully integrated with ChatGPT—you must return manually to continue the flow

⚠️ Occasional bugs, such as failing to re-engage after user input in certain sessions

Despite these, Operator is already valuable for:

Accessing portals that lack open APIs or modern exports

Giving users direct, secure control over their own data collection

Despite these limitations, Operator continues to evolve. Looking ahead, we’re excited for what may be coming:

✅ More automation (e.g., “check for new results weekly”)

✅ Tighter chat integration (seamless Operator ↔️ GPT loops)

✅ Smarter exports (batch tools, annotations, PDF generation)

⚙️ How We Built It
Like all our projects, this was co-built with AI.

Our team used:

A set of ChatGPT pods (like "ProductPod") for planning, testing, and comms

And for the first time, Codex Agents as our development arm

Codex agents had direct access to GitHub, used the CLI, and made fast, high-quality commits with precision. In just two days, they completed:

✨ 102 dev tickets (!!)

New features

Bug fixes

Backend + frontend enhancements

Watching the logs felt like seeing the future of software delivery.

⚠️ Bold, but Necessary
We know this is a bold post. It may raise eyebrows.

Some will ask: Did you just automate login to real health portals with an AI browser?

Yes—but only with consent, transparency, and human oversight.

This PoC is a test of what’s technically possible and what’s ethically defensible. We didn’t bypass security. We didn’t store credentials. We didn’t break Terms of Use.

We used a tool designed to simulate human interaction, acting only under human control, for a task humans are already allowed to do: downloading their own health data.

It’s time to have this conversation out loud.

🌏 What Comes Next
We’re now exploring:

Policy and regulatory compliance (PHIPA, PIPEDA)

Pilot partnerships with health orgs

Other use cases in government & broader public sector

But most of all, we’re looking for people who want to test, shape, and evolve this model.

The patient is the only one at every point of care. Let's give them tools to succeed.

Thanks again to Will and Jocelyne for pushing this one forward. This is just the beginning.