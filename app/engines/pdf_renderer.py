from datetime import datetime
from jinja2 import Template

PDF_TEMPLATE = """
Clinical Summary – Concussion Recovery Tracker
-------------------------------------------------
User ID: {{ user_id }}
Export Time: {{ now }}

{% if incident %}
Injury Date: {{ incident.injury_date }}
Reporter Role: {{ incident.reporter_role }}
Sport: {{ incident.sport_type }}
Age Group: {{ incident.age_group }}
Incident Context: {{ incident.injury_context }}
Cleared to Play: {{ incident.cleared_to_play }}
Lost Consciousness: {{ incident.lost_consciousness }}
Diagnosed Concussion: {{ incident.diagnosed_concussion }}
Still Symptomatic: {{ incident.still_symptomatic }}
Seen Provider: {{ incident.seen_provider }}
{% endif %}

{% if stage %}
Current Recovery Stage: {{ stage }}
{% endif %}


Symptom History:
{% for s in symptoms[-5:] %}
- {{ s.timestamp }} | {{ s.symptom_id }} ({{ s.severity }}) – {{ s.reporter_type or 'unknown' }}
  Notes: {{ s.extra_notes or 'n/a' }}
{% endfor %}
"""

def render_pdf(user_id: str, symptoms: list, stage: str = None, incident: object = None):
    tmpl = Template(PDF_TEMPLATE)
    return tmpl.render(user_id=user_id, symptoms=symptoms, stage=stage, incident=incident, now=datetime.utcnow().isoformat())