## 🧾 Section Prompt Contract (Iteration 3)

### 🧱 Prompt Structure
```
You are a policy analyst drafting a section for a government investment artifact.

Use the following context to generate a dense, structured, and strategic section draft.

=== Artifact Info ===
Artifact: {{ artifact.name }}
Section: {{ section.title }}

=== Section Definition ===
Purpose: {{ section.purpose }}
Description: {{ section.definition }}
Required Intents:
{% for intent in section.intents %}
- {{ intent }}
{% endfor %}

=== Project Profile ===
{{ project_profile_text }}

=== Global Research ===
{% if corpus_summary %}
[Corpus Summary]
{{ corpus_summary }}
{% endif %}
{% if web_results %}
[Web Search Summary]
{{ web_results }}
{% endif %}
{% if alignment_findings %}
[Strategic Alignment Insights]
{{ alignment_findings }}
{% endif %}

=== Prior Sections ===
{% if prior_sections_summary %}
{{ prior_sections_summary }}
{% else %}
(None yet)
{% endif %}

=== Instructions ===
- Address all required intents
- Use context, not repetition
- Integrate facts across research types
- Stay within 300-500 words unless otherwise specified
- Return clean Markdown content only
```

---

### 🔄 Variables
| Placeholder | Source |
|-------------|--------|
| `artifact.name`, `section.title` | From `gate_reference_v2.yaml` |
| `section.intents` | From section metadata |
| `project_profile_text` | Assembled string from project profile engine |
| `corpus_summary`, `web_results`, `alignment_findings` | From global context tools |
| `prior_sections_summary` | Summarized prior generated sections |

---

### ✅ Prompt Goals
- Align LLM with user-facing narrative
- Carry forward knowledge iteratively
- Encourage grounded, cohesive output
- Modular for testing + debug

---

### 🧪 Test Plan
Will validate against 2-section dry run and manually inspect:
- Prompt hydration
- Intent coverage
- Context usage
- Output quality