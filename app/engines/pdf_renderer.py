from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import requests
from datetime import datetime
import tempfile
import os

def render_pdf(user_id, stage, symptoms, metadata):
    """
    Generates a PDF summary from a template and returns the byte stream.
    """
    env = Environment(loader=FileSystemLoader("app/templates"))
    template = env.get_template("clinical_summary.html")

    html_out = template.render(
        user_id=user_id,
        export_date=datetime.now().strftime("%Y-%m-%d"),
        stage=stage,
        symptoms=symptoms,
        reporter_type=metadata.get("reporter_type", ""),
        incident_context=metadata.get("incident_context", ""),
        sport_type=metadata.get("sport_type", ""),
        age_group=metadata.get("age_group", ""),
        team_id=metadata.get("team_id", "")
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        HTML(string=html_out).write_pdf(f.name)
        with open(f.name, "rb") as result_file:
            pdf_bytes = result_file.read()
        os.unlink(f.name)

    return pdf_bytes