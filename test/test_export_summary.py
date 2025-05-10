from app.tools.export_summary import export_summary
from fastapi.testclient import TestClient
from main import app  # assumes app is defined in main.py

client = TestClient(app)

def test_export_summary_tool(monkeypatch):
    # Mock db fetch
    def mock_get_tracker_and_logs(user_id):
        return {
            'user_id': user_id,
            'state': {'stage': 'Stage 2'}
        }, [
            {'symptom_id': 'headache', 'severity': 3, 'timestamp': '2025-05-01T10:00:00Z'},
            {'symptom_id': 'nausea', 'severity': 2, 'timestamp': '2025-05-01T12:00:00Z'}
        ]

    monkeypatch.setattr("app.db.db_reader.get_tracker_and_logs", mock_get_tracker_and_logs)

    response = client.post("/export_summary", json={"user_id": "demo-user"})
    assert response.status_code == 200
    data = response.json()
    assert "pdf_url" in data
    assert data["pdf_url"].startswith("https://")
    assert "fhir_bundle" in data
    assert data["fhir_bundle"]["resourceType"] == "Bundle"
    assert any(e["resource"]["resourceType"] == "Observation" for e in data["fhir_bundle"]["entry"])