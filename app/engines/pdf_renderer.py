from datetime import datetime
from jinja2 import Template

TEMPLATE = """
<h2>Symptom Tracker Summary</h2>
<p><strong>Recovery Stage:</strong> {{ stage or 'Not recorded' }}</p>
<p><strong>Team:</strong> {{ team_id }} | <strong>Age:</strong> {{ age_group }} | <strong>Sport:</strong> {{ sport_type }}</p>
<p><strong>Reporter:</strong> {{ reporter_type }} | <strong>Context:</strong> {{ incident_context }}</p>
<p><strong>Logs:</strong></p>
<ul>
{% for s in symptoms %}
  <li>{{ s.timestamp }} - {{ s.symptom_id }} ({{ s.severity }})</li>
{% endfor %}
</ul>
"""

def render_pdf(symptoms: list, stage: str, context: dict):
    template = Template(TEMPLATE)
    html = template.render(
        symptoms=symptoms[-5:],  # show last 5
        stage=stage,
        team_id=context.get("team_id"),
        age_group=context.get("age_group"),
        sport_type=context.get("sport_type"),
        reporter_type=context.get("reporter_type"),
        incident_context=context.get("incident_context")
    )
    return html  # placeholder: return HTML string for now