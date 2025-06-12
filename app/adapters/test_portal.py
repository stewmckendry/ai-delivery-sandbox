from __future__ import annotations

from pathlib import Path
from typing import Dict, List


def scrape_test_portal(*_args, **_kwargs) -> Dict[str, List[str]]:
    """Return paths to sample HTML and PDF files for testing."""
    base = Path(__file__).resolve().parents[2] / "tests" / "sample_data"
    html = base / "visit.html"
    pdf = base / "labs.pdf"
    if not base.exists():
        base.mkdir(parents=True, exist_ok=True)
        # create simple files if missing
        html.write_text(
            "<div class='visit'><span class='date'>2023-01-01</span>"
            "<span class='provider'>Clinic</span><span class='doctor'>Dr. Z" \
            "</span><p class='notes'>Test</p></div>",
            encoding="utf-8",
        )
        # reuse helper from e2e_test_runner to create a small PDF
        from scripts.e2e_test_runner import create_sample_pdf

        create_sample_pdf(pdf)
    return {"files": [str(html), str(pdf)]}
