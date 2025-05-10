from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import requests
from datetime import datetime
import tempfile
import os

TEMPLATE_URL = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/app/templates/clinical_summary.html"

def render_pdf(user_id, stage, symptoms):
    """
    Renders a concussion recovery summary PDF from user data.
    Returns path to generated PDF file.
    """
    # Fetch template from GitHub
    response = requests.get(TEMPLATE_URL)
    response.raise_for_status()
    template_content = response.text

    # Write template to temp file
    env = Environment(loader=FileSystemLoader(tempfile.gettempdir()))
    template_path = os.path.join(tempfile.gettempdir(), "clinical_summary.html")
    with open(template_path, "w", encoding="utf-8") as f:
        f.write(template_content)
    template = env.get_template("clinical_summary.html")

    # Render and generate PDF
    rendered_html = template.render(
        user_id=user_id,
        export_date=datetime.now().strftime('%Y-%m-%d'),
        stage=stage,
        symptoms=symptoms
    )

    pdf_path = os.path.join(tempfile.gettempdir(), f"summary_{user_id}.pdf")
    HTML(string=rendered_html).write_pdf(pdf_path)
    return pdf_path