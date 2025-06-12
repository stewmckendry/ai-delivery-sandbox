"""PDF parser utilities using PyMuPDF (fitz) to extract lab results."""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict

import fitz  # PyMuPDF


def extract_lab_results(pdf_path: str | Path) -> List[Dict[str, str]]:
    """Parse the PDF at ``pdf_path`` and return structured lab results.

    Parameters
    ----------
    pdf_path: str | Path
        Path to the PDF file containing lab results.

    Returns
    -------
    List[Dict[str, str]]
        A list where each dict contains ``test_name``, ``value`` and ``units``.
    """

    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    results: List[Dict[str, str]] = []

    with fitz.open(path) as doc:
        text = ""
        for page in doc:
            text += page.get_text("text")

    # simple heuristics: assume each line may contain a test result formatted as
    # "<test name> <value> <units>". This spike does not handle complex layouts.
    for line in text.splitlines():
        parts = line.strip().split()
        if len(parts) < 3:
            continue
        # last item is units, preceding item is value, rest is test name
        *name_parts, value, units = parts
        if not value.replace('.', '', 1).isdigit():
            continue
        test_name = " ".join(name_parts)
        results.append({
            "test_name": test_name,
            "value": value,
            "units": units,
        })

    return results
