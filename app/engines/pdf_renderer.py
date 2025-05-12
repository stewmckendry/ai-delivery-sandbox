from datetime import datetime
from jinja2 import Template

PDF_TEMPLATE = """
Clinical Summary – Concussion Recovery Tracker
-------------------------------------------------
User ID: {{ user_id }}
Export Time: {{ now }}

{% if stage %}Current Recovery Stage: {{ stage }}{% endif %}


Symptom History:
{% for s in symptoms[-5:] %}
- {{ s.timestamp }} | {{ s.symptom_id }} ({{ s.severity }}) – {{ s.reporter_type or 'unknown' }}
{% endfor %}
"""

def render_pdf(user_id: str, symptoms: list, stage: str = None):
    tmpl = Template(PDF_TEMPLATE)
    return tmpl.render(user_id=user_id, symptoms=symptoms, stage=stage, now=datetime.utcnow().isoformat())