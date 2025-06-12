"""Lab PDF parser to extract structured lab results."""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Dict, Optional

import fitz  # PyMuPDF


DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def extract_lab_results_with_date(pdf_path: str | Path) -> List[Dict[str, Optional[str]]]:
    """Parse lab results from ``pdf_path`` and include dates when available.

    Parameters
    ----------
    pdf_path: str | Path
        The path to the PDF file containing lab results.

    Returns
    -------
    List[Dict[str, Optional[str]]]
        List of dictionaries with ``test_name``, ``value``, ``units`` and
        optional ``date`` field.
    """

    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    results: List[Dict[str, Optional[str]]] = []

    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text("text")

    for line in text.splitlines():
        parts = line.strip().split()
        if len(parts) < 3:
            continue

        date: Optional[str] = None
        # Check for date pattern in last token
        if DATE_RE.fullmatch(parts[-1]):
            date = parts[-1]
            units = parts[-2]
            value = parts[-3]
            name_tokens = parts[:-3]
        else:
            units = parts[-1]
            value = parts[-2]
            name_tokens = parts[:-2]

        if not value.replace('.', '', 1).isdigit():
            continue

        test_name = " ".join(name_tokens)
        results.append({
            "test_name": test_name,
            "value": value,
            "units": units,
            "date": date,
        })

    return results
