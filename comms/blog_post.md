MyHealth AI Assistant: Helping You Compile and Make Sense of Your Health Information
This blog explores how intelligent AI assistance can empower patients and rethink interoperability across the healthcare ecosystem

By Stewart McKendry, Jocelyne Verity, and Will Falk

Welcome to the seventh post in Coaching the Machine, where we explore how humans and AI can build together.

This post is a collaboration with two exceptional people in healthcare: Jocelyne Verity and Will Falk. Both are seasoned healthcare executives, policy leaders, and champions for system transformation in Canada. This post wouldn’t exist without their curiosity, feedback, and encouragement.

Many of us (the authors included) have worked on electronic health record strategies, standards, and infrastructure for years. We’ve contributed to regional initiatives, national blueprints, provider adoption, and digital health innovation.

However, this post isn’t about critiquing that work. It’s about reimagining what interoperability can look like today. With tools like MyHealth AI Assistant, the integration point isn’t only a shared backend—it’s the patient. Supported by an intelligent assistant, patients can compile, interpret, and carry their records throughout their care journey. This shift deserves serious consideration, creative exploration, and open policy discussion.

What If You Had a Personal Health Concierge?
"I’m a caregiver for my dad with dementia. I’m usually organized, but I can’t keep up. Every appointment means a new portal and another login. Even when I have the information, I’m not always sure what it means or how to use it to support his care. I feel like I’m chasing pieces of a puzzle I can’t put together."

That’s the reality for many Canadians, especially family or informal caregivers.

Family caregivers often juggle:

Coordinating with multiple providers, each with different records and responsibilities

Managing lab results, imaging reports, and medication updates

Navigating complex PDFs filled with jargon from disconnected systems

Health data is becoming more accessible to patients through various online portals—whether it’s MyChart for hospital records, test results from LifeLabs or Dynacare, prescriptions via Shoppers or Rexall, or provincial portals like Alberta’s MyHealth Records, BC’s Health Gateway, Saskatchewan’s MySaskHealthRecord, and Ontario’s ConnectMyHealth.

These tools are secure and well-intentioned, but they remain siloed. Patients are left to navigate these systems on their own, often struggling to make sense of the information they find.

That’s where MyHealth AI Assistant comes in. It’s a secure digital assistant designed to help users retrieve their health information from various providers and portals, understand it in clear, plain language, and use it to support care planning and decision-making. Instead of waiting for every system to connect through a central platform, the Assistant flips the model. The patient becomes the point of integration.

This isn’t the first attempt to give patients control over their health data—Microsoft’s HealthVault tried something similar in the 2010s but struggled without widespread integration. The difference now is AI. Today’s AI assistants don’t just store data; they reason, take action, and adapt in real-time to handle the messiness of real-world information.

Meet MyHealth AI Assistant
MyHealth AI Assistant brings two key capabilities to users: using Operator (from OpenAI) to help patients compile their health records from multiple providers and portals, and utilizing a custom-built ChatGPT for tasks like asking questions, summarizing records, and preparing for appointments.

OpenAI Operator: Operator is a real-time browser tool that navigates various health portals with the user’s explicit consent, retrieving and compiling health information. It’s not scraping data or automating tasks behind the scenes; instead, it assists the user in compiling their records in a transparent, human-in-the-loop process.

Custom ChatGPT: Alongside Operator, the custom ChatGPT takes over when the patient wants to interact with their records. It answers questions, helps understand complex medical terms, and can prepare summaries for appointments. It’s the language superpower that provides support when navigating through confusing health information.

Think of the assistant as AI working within the scope of the patient, or a tech-savvy family caregiver. And in some cases, it could be permitted by the treating physician as part of shared care planning.

How It Works
Here’s how the MyHealth Assistant works, as demonstrated in a real-world test:

The user initiates a request
The experience begins with a prompt like: “Help me collect my recent health records.” For this demonstration, one of the authors consented to use their own data from three live systems: a personal health and fitness app, a national laboratory provider, and a hospital portal powered by MyChart.

Operator launches to assist with record collection
The Assistant launches OpenAI Operator to begin gathering records. The user manually logs into each health portal, with Operator pausing at each step to ensure full user control. At no point are credentials stored or visible to the Assistant.

The user navigates and approves record selection
Once inside the portals, Operator assists in locating relevant records. The user approves each record to retrieve. Every action is transparent, interruptible, and under the user’s direct supervision.

Health records are uploaded securely
After the user confirms, records are uploaded using a session-specific, signed link. Files are processed securely, with no data retained outside the user’s session.

Records are parsed and structured
In the backend, health records are extracted, cleaned, and organized into clinically relevant types like patient and provider information, encounters, labs, diagnostics, imaging, and conditions. Where possible, standard medical codes like SNOMED CT are used to preserve meaning and enable downstream sharing.

Records are indexed for semantic search
All structured records are embedded into a Chroma vector store, enabling semantic retrieval by topic or question. This creates a personalized, searchable health record, compiled entirely under the user’s control.

The user asks questions or explores their health information
With data structured and indexed, the Assistant can now answer natural language questions:

User: “Do I show signs of being low on iron?”
AI Assistant: “Yes. Your ferritin level is 27 µg/L, which is below the normal range. This suggests iron deficiency. Would you like help preparing a summary or questions for your doctor?”

User: “I hurt my finger recently and remember breaking it before. Can you find anything?”
AI Assistant: “Yes. A December 2019 imaging report shows a healing fracture in your right fourth finger’s middle phalanx.”

The Assistant supports understanding and sharing
Beyond Q&A, the Assistant can summarize long reports, explain medical terms in plain language, and generate visit-ready summaries complete with citations from the original record. The user ends the session with greater clarity, confidence, and control over their health and better equipped to support the care of others.

Who This Helps
Patients: Want better access, clarity, and control over their health data. The Assistant helps them compile records from multiple sources, explains medical terms, and supports decision-making. More importantly, it builds confidence and health literacy.

Clinicians: Can treat the summaries as context to cross-reference, not replace. Over time, this could reduce administrative friction, flag potential follow-ups, and lead to more productive conversations during visits.

Administrators & Policymakers: Working under pressure with growing patient needs and budget constraints. Tools like the Assistant help patients help themselves, reducing support requests, and improving continuity of care.

People, Privacy & Compliance: Strengths and Gaps
People
The user remains in control throughout the process, deciding how their health data is accessed, interpreted, and used with the help of the AI assistant. However, digital literacy varies across populations, with some patients needing assistance. Healthcare providers are also impacted by these tools and require systems that integrate smoothly into their workflows.

Strengths: The system ensures clear consent and transparency, with users guiding the AI assistant’s actions. This human-in-the-loop design fosters trust and allows users to maintain control over their health data.

What’s needed: Ongoing consultation and design efforts to ensure the system works for diverse demographics. Testing across a range of needs and improving usability for both patients and providers will help ensure accessibility and build trust in the system.

Privacy & Security
Credentials are never stored, and health records are processed only within a user-scoped session using encrypted links and access-controlled storage. The system emphasizes transparency and control, with users initiating each step, giving explicit consent, and ensuring no health data is shared outside their session.

Strengths: The system supports a privacy-first approach with session-scoped processing, short-lived storage, encrypted uploads, and secure token-based API access. Users maintain control throughout the workflow, from Operator to GPT.

What’s needed: To meet clinical and institutional expectations, the system would benefit from fine-grained record deletion and tools explaining data use. A third-party security review and alignment with regulatory standards like PHIPA or HIPAA would strengthen trust and adoption.

Legal & Compliance
As AI becomes more integrated into healthcare, legal frameworks such as Ontario’s Personal Health Information Protection Act (PHIPA) must evolve to address how personal health information (PHI) is accessed, interpreted, and used in AI-assisted workflows.

Strengths: The system is consent-driven, with users initiating and approving all access to their health data. Manual workflows ensure data is only handled under user control, minimizing risks of unintended automation or third-party exposure.

What’s needed: Enforceable pilot programs are needed to test responsible AI use within healthcare settings under clear safeguards. Terms of service should clarify acceptable AI use, and collaboration with regulators like Ontario’s Information and Privacy Commissioner (IPC) is essential to define compliance standards.

How We Built It
As with our past projects, we built this prototype with help from AI itself. We used ProductPods (custom ChatGPTs wired with GitHub that help build and ship apps) for planning, design and managing the work.

The difference this time was using OpenAI Codex Agents, which handled 135 development tasks in 4 days—delivering new features, enhancements, bug fixes, design docs, deployment plans, scripts, and more! The velocity and precision/quality were impressive, not to mention being able to see the reasoning trace of what steps the agents took and why, watching them run commands in CLI on screen.

What Comes Next
The MyHealth AI Assistant is live! If you'd like to try it and share feedback, please send a message to the authors. Caveat emptor—this is an early proof of concept (PoC) and rough around the edges. Operator is still in preview and requires a Pro license, but the rest of the Assistant is available with a Plus subscription.
See the [User Access Guidance](../project/docs/user_access_guidance.md) for how to experiment safely with or without Operator.

Natural next steps include exploring policy and regulatory engagement, piloting use cases, and expanding applications in the public sector. These efforts will help shape the future of the system and ensure broader adoption and alignment with industry standards.

The patient is the only person at every point of care. Let’s give them tools to succeed.