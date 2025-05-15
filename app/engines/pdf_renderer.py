from weasyprint import HTML
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
import tempfile, uuid, os

def render_pdf(data):
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
        <p><strong>User ID:</strong> {data['user_id']}</p>
        <p><strong>Generated:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>

        <h2>Incident Summary</h2>
        <ul>
            {''.join(f'<li><strong>{k}:</strong> {v}</li>' for k, v in data['incident'].items())}
        </ul>

        <h2>Stage Guidance</h2>
        <p><strong>Stage:</strong> {data['stage']['stage_name']}</p>
        <p>{data['stage']['stage_summary']}</p>

        <h3>What You Can Do</h3>
        <ul>
            {''.join(f'<li>{a}</li>' for a in data['stage']['allowed_activities'])}
        </ul>

        <h3>How to Progress</h3>
        <ul>
            {''.join(f'<li>{p}</li>' for p in data['stage']['progression_criteria'])}
        </ul>

        <h2>Symptom History</h2>
        <ul>
            {''.join(f"<li>{s['timestamp']}: {s['symptom_id']} = {s['score']}</li>" for s in data['symptoms'])}
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
