from weasyprint import HTML
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
import tempfile, uuid, os
from sqlalchemy.orm import class_mapper

def to_dict_readable(model_obj):
    raw = {c.key: getattr(model_obj, c.key) for c in class_mapper(model_obj.__class__).columns}
    label_map = {
        "user_id": "User",
        "timestamp": "Reported On",
        "reporter_role": "Reported By",
        "sport_type": "Sport",
        "age_group": "Age Group",
        "team_id": "Team",
        "injury_date": "Injury Date",
        "injury_context": "Incident Description",
        "lost_consciousness": "Lost Consciousness",
        "seen_provider": "Saw Medical Provider",
        "diagnosed_concussion": "Diagnosed Concussion",
        "still_symptomatic": "Still Has Symptoms",
        "cleared_to_play": "Cleared to Play"
    }
    return {label_map.get(k, k): v for k, v in raw.items() if v is not None}

def render_pdf(data):
    incident = data.get('incident') or {}
    incident_dict = to_dict_readable(incident) if incident else {}
    stage = data.get('stage') or {}
    symptoms = data.get('symptoms') or []

    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; padding: 2em; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ margin-top: 1.5em; color: #34495e; }}
            ul {{ padding-left: 1.2em; }}
            li {{ margin-bottom: 0.4em; }}
        </style>
    </head>
    <body>
        <h1>Concussion Recovery Summary</h1>
        <p><strong>Generated:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>

        <h2>What Happened?</h2>
        <ul>
            {''.join(f'<li><strong>{k}:</strong> {v}</li>' for k, v in incident_dict.items()) or "<li>No incident data provided.</li>"}
        </ul>

        <h2>Recovery Guidance</h2>
        <p><strong>Stage:</strong> {stage.get('stage_name', 'N/A')}</p>
        <p>{stage.get('stage_summary', 'No summary available.')}</p>

        <h3>What You Can Do</h3>
        <ul>
            {''.join(f'<li>{a}</li>' for a in stage.get('allowed_activities', [])) or "<li>Not specified</li>"}
        </ul>

        <h3>How to Progress</h3>
        <ul>
            {''.join(f'<li>{p}</li>' for p in stage.get('progression_criteria', [])) or "<li>Not specified</li>"}
        </ul>

        <h2>Symptom History</h2>
        <ul>
            {''.join(f"<li>{s.timestamp}: {s.symptom_id} = {s.score}</li>" for s in symptoms) or "<li>No symptoms logged.</li>"}
        </ul>

    </body>
    </html>
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        HTML(string=html_content).write_pdf(tmp_pdf.name)
        pdf_path = tmp_pdf.name

    blob_name = f"summary_{uuid.uuid4().hex}.pdf"
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = "exports"

    blob_service = BlobServiceClient.from_connection_string(conn_str)
    blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)

    with open(pdf_path, "rb") as f:
        blob_client.upload_blob(f.read(), overwrite=True)

    sas_token = generate_blob_sas(
        account_name="concussionexports",
        container_name=container_name,
        blob_name=blob_name,
        account_key=os.getenv("AZURE_STORAGE_ACCOUNT_KEY"),
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )

    return f"https://concussionexports.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
