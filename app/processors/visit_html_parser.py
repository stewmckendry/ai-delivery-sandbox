"""HTML parser for extracting visit summaries."""

from __future__ import annotations

from typing import List, Dict

from bs4 import BeautifulSoup


def extract_visit_summaries(html: str) -> List[Dict[str, str]]:
    """Parse ``html`` and return visit summaries.

    Parameters
    ----------
    html: str
        HTML content containing visit summary entries.

    Returns
    -------
    List[Dict[str, str]]
        Each dict contains ``date``, ``provider``, ``doctor`` and ``notes``.
    """

    soup = BeautifulSoup(html, "html.parser")
    visits: List[Dict[str, str]] = []

    for section in soup.select("div.visit"):
        date_el = section.select_one(".date")
        provider_el = section.select_one(".provider")
        doctor_el = section.select_one(".doctor")
        notes_el = section.select_one(".notes")

        visits.append(
            {
                "date": date_el.get_text(strip=True) if date_el else "",
                "provider": provider_el.get_text(strip=True) if provider_el else "",
                "doctor": doctor_el.get_text(strip=True) if doctor_el else "",
                "notes": notes_el.get_text(strip=True) if notes_el else "",
            }
        )

    return visits
