"""Utility helpers to generate small sample files for tests and demos."""
from __future__ import annotations

from pathlib import Path


def create_sample_pdf(path: Path) -> None:
    """Create a simple PDF with two lab result lines."""
    import fitz  # PyMuPDF

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Cholesterol 5.8 mmol/L 2023-05-01")
    page.insert_text((72, 90), "Hemoglobin 13.5 g/dL 2023-05-02")
    doc.save(path)
    doc.close()


def create_sample_html(path: Path) -> None:
    """Create simple HTML with a single visit summary."""
    html = """
    <html><body>
      <div class='visit'>
        <span class='date'>2023-06-01</span>
        <span class='provider'>General Hospital</span>
        <span class='doctor'>Dr. Jones</span>
        <p class='notes'>Routine check</p>
      </div>
    </body></html>
    """
    path.write_text(html, encoding="utf-8")
