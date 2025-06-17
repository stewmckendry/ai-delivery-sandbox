# Beyond Health: How AI Copilots Could Transform Public Services

Imagine every Canadian having a digital assistant to help navigate government services—from student loans to immigration applications—with the clarity of a human and the speed of AI.

This vision combines two technologies:

- **OpenAI Operator:** A secure, human-in-the-loop AI that assists users in logging in and navigating online portals (no backend integration required).
- **ChatGPT:** A conversational assistant that explains documents, answers questions, and helps complete tasks in plain language.

Together, they create an AI Copilot for government services—working alongside citizens, not behind the scenes. This article explores the concept, Canadian use cases, and what’s needed for responsible deployment.

---

## 👩‍💻 The Big Idea

Many Canadians struggle to access and understand government data:

- Portals are complex, outdated, or fragmented.
- Key information is hidden in PDFs, technical language, or scattered across systems.
- High-need users (seniors, newcomers, low-income individuals) face the greatest barriers.

Instead of waiting for centralized integrations, this approach lets the **user be the integration point**. By combining Operator + GPT, people can securely collect and understand their own data—instantly, privately, and on their terms.

---

## 🔍 Where Could This Help Most?

We identified several Canadian public-sector systems where this AI copilot pattern could have real impact:

### 🧾 1. CRA MyAccount – Taxes & Benefits
- Operator logs in and retrieves notices, benefits, and return history.
- GPT explains refunds, tax balances, or benefit eligibility in plain English.
- **Impact:** Reduces digital friction, especially for seniors and low-literacy users.
- **Risk:** Privacy and compliance—CRA currently forbids automation.

### 🛂 2. IRCC Portals – Immigration & Citizenship
- Operator checks for document requests or application status.
- GPT summarizes letters and suggests next steps.
- **Impact:** Reduces anxiety and errors in complex processes.
- **Risk:** Legal exposure if AI advice is incorrect; fragile systems.

### 🎓 3. OSAP + NSLSC – Student Aid & Loans
- Operator fetches loan/grant info across federal/provincial systems.
- GPT explains repayments, timelines, and financial literacy tips.
- **Impact:** High; clear use case with tech-savvy users.
- **Status:** Most ready for a real-world pilot.

### 🏠 4. Ontario Works / ODSP – Social Support
- Operator reports income, checks letters, uploads documents.
- GPT explains benefit letters and deadlines in simple or preferred language.
- **Impact:** Crucial accessibility for vulnerable users.
- **Design note:** Prioritize trust, consent, and equity.

### 🎖 5. Veterans Affairs – My VAC Account
- Operator tracks benefits, new letters, appointments.
- GPT explains service decisions or helps with appeals.
- **Impact:** Supports veterans overwhelmed by bureaucracy.

### ⚖️ 6. Courts & Legal – Small Claims, E-Filing
- Operator logs in and tracks court case status.
- GPT drafts plain-language summaries and legal forms.
- **Impact:** Improves access to justice for self-represented litigants.
- **Challenge:** Must avoid unauthorized legal advice.

---

## ✅ Benefits

- **Empowers users:** Makes portals more accessible, especially for those facing barriers.
- **Reduces support burden:** Handles common questions and tasks now managed by call centers.
- **Improves outcomes:** Prevents missed deadlines or lost benefits due to confusion.
- **Accelerates modernization:** No backend integration or system overhaul required.

---

## ⚠️ Risks & Mitigations

| Risk                  | Example                                      | Mitigation                                      |
|-----------------------|----------------------------------------------|-------------------------------------------------|
| Privacy               | Mishandled credentials or personal data      | Human-in-the-loop consent, encryption, audits   |
| Incorrect AI response | GPT misreads a tax letter or legal deadline  | Guardrails, disclaimers, human escalation       |
| Unauthorized access   | Agent logs in as wrong user or is spoofed    | MFA, session-based access                       |
| Policy misalignment   | Scraping portals violates terms of use       | Agency partnerships, sandbox pilots             |

---

## 🧭 Enabling Success

- **Explicit User Consent:** All data access is user-initiated; no scraping or stored credentials.
- **Secure AI Infrastructure:** Encrypted, ephemeral, and auditable sessions; AI only sees what the user sees.
- **Scope Discipline:** GPT explains and summarizes—does not prescribe or decide. Human review for legal/financial matters.
- **Agency Collaboration:** Agencies can approve or support assistants, starting with “read-only” tasks.
- **Clear User Value:** Immediate benefits for users, especially those with challenges.

---

## 🚀 What’s Next?

A pilot in student loans or housing support could quickly and safely demonstrate this model at scale. These areas:

- Are high-friction, high-need
- Have clear technical feasibility
- Serve user groups who would benefit most

From there, the model could expand across sectors—with safeguards and design principles that prioritize user trust.

---

## Final Word

As people expect services to work like their favorite apps, government must meet them where they are. Secure automation and smart conversation can make government more human—one session at a time.
