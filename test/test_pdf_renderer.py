from app.engines.pdf_renderer import render_pdf
import os

def test_render_pdf_creates_file():
    user_id = "testuser"
    stage = "Stage 2"
    symptoms = [
        {"symptom_id": "headache", "severity": 4, "timestamp": "2025-05-01T10:00:00Z"},
        {"symptom_id": "fatigue", "severity": 2, "timestamp": "2025-05-01T12:00:00Z"}
    ]

    pdf_path = render_pdf(user_id, stage, symptoms)
    assert os.path.exists(pdf_path)
    assert pdf_path.endswith(".pdf")
    assert os.path.getsize(pdf_path) > 1000  # at least 1KB of output

    # Cleanup temp file
    os.remove(pdf_path)