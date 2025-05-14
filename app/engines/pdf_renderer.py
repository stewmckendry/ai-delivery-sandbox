from jinja2 import Template

template = Template("""
Recovery Summary for {{ user_id }}

---

📅 Incident Date: {{ incident.injury_date.strftime('%Y-%m-%d') if incident else 'N/A' }}
📝 Context: {{ incident.injury_context if incident else 'N/A' }}
🏀 Sport: {{ incident.sport_type if incident else 'N/A' }}
👥 Age Group: {{ incident.age_group if incident else 'N/A' }}

---

📊 Symptoms:
{% for s in symptoms[:10] %}- {{ s.symptom_id }}: {{ s.score }} {% if s.notes %} ({{ s.notes }}) {% endif %}
{% endfor %}

---

📈 Current Stage: {{ stage.name if stage else 'N/A' }}
✅ Activities: {{ ", ".join(stage.allowed_activities) if stage else 'N/A' }}
📍 Criteria: {{ ", ".join(stage.progression_criteria) if stage else 'N/A' }}

---

🧪 Last Activity Check-in:
Stage Attempted: {{ activity.stage_attempted if activity else 'N/A' }}
Worsened: {{ 'Yes' if activity and activity.symptoms_worsened else 'No' if activity else 'N/A' }}

---

"""
)

def render_pdf(user_id, symptoms, stage, incident, activity):
    return template.render(
        user_id=user_id,
        symptoms=symptoms,
        stage=stage,
        incident=incident,
        activity=activity
    )