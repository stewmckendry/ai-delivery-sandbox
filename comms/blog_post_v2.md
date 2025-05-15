# How a Custom Concussion GPT Agent Could Transform Youth Sports Safety in Ontario

**By Stewart McKendry and Jocelyne Verity**

---

## 🏋️️ Introducing the Use Case Series

This post is the first in a new series exploring how AI-powered GPT agents can be applied to solve real-world problems — starting with health, sport, and youth wellbeing.

For this proof-of-concept (PoC), I (Stewart) partnered with **Jocelyne Verity**, a health executive with 15 years of experience spanning PwC, EY, Canadian Mental Health Association, and Southlake Regional Health Centre. Together, we’re collaborating on AI advisory with a purpose — using AI for good.

---

## 🚤 The Hidden Threat: Concussions in Youth Sport

Each year, thousands of young athletes in Ontario face a hidden threat on the field, rink, or court: concussions. These brain injuries are often underreported, misunderstood, and mismanaged—not due to a lack of concern, but due to a lack of accessible, consistent tools and support.

In Ontario, **Rowan’s Law** has made concussion awareness and return-to-play protocols a legal obligation. Still, there remains a major gap in real-time, accessible concussion support. Several national sport organizations—including Nordiq Canada, Canada Soccer, and the Canadian Junior Hockey League—have implemented formal concussion protocols requiring injury reporting and medical clearance before athletes return to play. These efforts align with **Sport Canada** mandates and the **Canadian Guideline on Concussion in Sport**, developed by **Parachute Canada** with the **Public Health Agency of Canada**. Over 50 NSOs have collaborated with Parachute to adopt standardized concussion policies, signaling a nationwide commitment to athlete safety and injury surveillance.

This app was born from real challenges seen both on the field and in the clinic:

* Parents and coaches often don’t know what counts as a concussion. “My head hurts”—is it serious or not?
* Families turn to endless Google searches, unsure which advice to trust. They ask: What can my child do? When can they go back? Is it safe?
* There’s a growing demand for structured injury reporting and return-to-play compliance.
* Health professionals are often left out of the loop, lacking structured symptom and recovery data when they see the patient.

---

## 🧠 Meet the Concussion Recovery GPT

We’ve built a prototype of a custom **ChatGPT agent** designed specifically to support concussion management in youth sports. This tool isn’t just a chatbot — it’s an intelligent, structured digital assistant that guides parents, coaches, and players through symptom checking, recovery tracking, and safe return-to-sport protocols grounded in clinical standards like **SCAT6** and national sport org guidelines.

> Importantly, ConcussionGPT is **not a doctor** — and it will say so. It is a support tool that helps users access existing medical knowledge and guidelines in a way that is **personalized, conversational, and easy to understand**.

### What it does:

* Helps assess potential concussions through guided Q\&A
* Logs symptoms and recovery progress day by day
* Provides stage-specific return-to-play advice
* Shares structured reports with healthcare professionals
* Offers anonymized insights to sports organizations

> “This isn’t just another form or chatbot. It’s a smart assistant that helps the right people take the right actions — at the right time.”

---

## 📸 What It Looks Like in Action

* A coach notices a collision on the field → GPT guides the assessment → logs the incident and starts recovery tracking.
* A parent checks in daily → logs symptoms and activity → system advises when to progress to the next stage.
* A doctor receives a structured timeline before the visit → reviews trends, makes a call on clearance.
* A sport system leader pulls quarterly concussion stats → identifies risks by sport and age group.

All journeys start with a simple prompt: *"Are you logging a new injury or checking in on an existing one?"* Or someone can just engage ConcussionGPT to ask questions about when their child can play soccer with their friends again.

> *(Placeholder: Stewart to add links and screenshots — chat transcript + dashboard views)*

---

## ⚙️ What’s Under the Hood

This isn't just a GPT front-end. It’s built using the **AI Delivery Framework** — a modular engineering process combining:

* Custom GPT that orchestrates triage, logging, and recovery chat
* Tools like `assess_concussion`, `get_triage_flow`, `log_incident_detail`, `get_stage_guidance`, and more, wired to the GPT
* FastAPI backend connected via OpenAPI schema
* Typed models using **Pydantic** and **SQLAlchemy** for **data validation** (ensuring quality data in the right format)
* Reference files grouped into:

  * **Structured "form" files** (e.g., `triage_map.yaml`, `checkin_map.yaml`) containing pick lists, branching logic, input types, and prompt guardrails to guide GPT conversations
  * **Medical knowledge graphs** (e.g., `symptoms_physical.yaml`, `stages.yaml`) grounded in concussion science, sourced from journals and tools like **Pathway.md**
* **Azure SQL database** for storing structured, anonymized recovery logs
* **Azure Blob Storage** for exporting PDFs and clinician-ready reports
* **Power BI dashboards** with filters by sport, age group, stage, and time
* **FHIR-compatible export** to send structured data to systems like Epic

This architecture enables **data validation at every step**, with transparent and auditable flows from user input → guidance → report.

---

## 💬 Rethinking the User Experience

Forget static forms and vague Google searches.

Users interact in plain language, with the GPT adapting tone, speed, and style based on who’s using it — a concerned parent, a young athlete, or a volunteer coach. The system avoids jargon, gives stepwise guidance, and flags when it’s time to seek professional care.

We’re also reinventing what a form looks like:

* No more PDFs or paper checklists
* Instead: conversational data collection, real-time feedback, and fewer errors from misinterpretation

This interactive model reduces back-and-forth, captures better data, and gives users more confidence.

> We’ll explore this deeper in future posts — and other use cases where we use forms all the time (think: screening tools in mental health, housing support applications, disability benefits, public intake portals…).

---

## 🛠️ The Build Process

We built this app using the **AI Delivery Framework** — a delivery team of GPT Pods:

* **ProductPods** to spec flows and features
* **QAPods** to validate every tool and stage
* **ResearchPods** to ground everything in medical evidence

This was a **human-led** project, co-piloted with our GPT Pods. **Jocelyne and Stewart** defined direction and scope, while the GPT Pods generated tools, code, flows, and documentation that we reviewed, edited, and tested together.

We started this project on a **Friday** and shipped the working prototype by **Wednesday** — with a weekend break and a few other work tasks in between. It’s a demonstration of just how quickly a useful, well-documented, and testable solution can be built.

The process followed a full arc — **discovery → iterative build → E2E testing → deployment** — all inside ChatGPT, with just a little GitHub, VSCode, Azure Portal, and Data Studio for good measure.

---

## 🚧 Adoption Barriers We’re Tackling

No innovation is without challenges. We’re working through:

* **Privacy & Security**: All data is anonymized, stored securely on Azure, and shared only with consent
* **Change Management**: Adoption support for coaches, families, leagues
* **Equity**: Designed for users who might not have wearables or tech confidence
* **Clinical Boundaries**: This is not a diagnostic tool — it’s a support system, built to complement, not replace, professional care

---

## 📍 What’s Next

We’re just getting started.

Coming next:

* Mobile deployment
* Deeper EMR integrations
* Broader rollout in schools, clubs, rec leagues
* New use cases in sprains, heat illness, sleep disorders, youth anxiety screening, and more

---

## 🏆 The Bottom Line

Ontario is already leading in concussion policy with Rowan’s Law. Now we have a chance to lead in practical, tech-enabled solutions too.

* An AI-powered concussion GPT agent offers real-time guidance, better care coordination, and rich data for safer sport. With thoughtful implementation, it could become a vital part of how we protect young athletes and support their full recovery.
* Are you a coach, physician, or sports administrator in Ontario? I’d love to connect. Let’s build something safer — together.

---

## 📣 Want to Try or Collaborate?

We’d love your feedback.

* 📅 **Try ConcussionGPT here**: \[link to app]
* 🎥 **Sign up for a live demo + Q\&A**: \[webinar link]
* 📩 **Reach us**: Stewart ([stewart.mckendry@gmail.com](mailto:stewart.mckendry@gmail.com)) + Jocelyne ([jeverity@gmail.com](mailto:jeverity@gmail.com))
* 🔍 **Want to co-create the next use case? Let’s talk.**
