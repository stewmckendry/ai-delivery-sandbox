import os
from pathlib import Path
import fitz
from app.processors.lab_pdf_parser import extract_lab_results_with_date


def create_sample_pdf(tmp_path: Path) -> Path:
    """Create a small PDF with two lab results."""
    file_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    # line with date
    page.insert_text((72, 72), "Cholesterol 5.8 mmol/L 2023-05-01")
    # second line without date
    page.insert_text((72, 90), "Hemoglobin 13.5 g/dL")
    doc.save(file_path)
    doc.close()
    return file_path


def test_extract_lab_results_with_date(tmp_path):
    pdf = create_sample_pdf(tmp_path)
    results = extract_lab_results_with_date(pdf)
    assert len(results) == 2
    assert results[0]["test_name"] == "Cholesterol"
    assert results[0]["value"] == "5.8"
    assert results[0]["units"] == "mmol/L"
    assert results[0]["date"] == "2023-05-01"
    assert results[1]["test_name"] == "Hemoglobin"
    assert results[1]["date"] is None
