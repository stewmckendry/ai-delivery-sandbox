from __future__ import annotations

import json
from typing import List, Dict

import openai
from bs4 import BeautifulSoup


PROMPT_TEMPLATE = (
    "Extract only patient-relevant content from this page. "
    "Classify it as one of: lab_result, visit_note, imaging_report, billing_info. "
    "Return JSON array of objects with keys 'type' and 'text'.\n"
    "Page content:\n{chunk}"
)


def _clean_html(html: str) -> str:
    """Return visible text from ``html`` using BeautifulSoup."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(" ", strip=True)


def _chunk_text(text: str, max_chars: int) -> List[str]:
    """Split ``text`` into chunks of ``max_chars`` length."""
    if max_chars <= 0:
        return [text]
    return [text[i : i + max_chars] for i in range(0, len(text), max_chars)]


def extract_relevant_content(
    html: str,
    source_url: str,
    *,
    max_chunk_chars: int = 4000,
) -> List[Dict[str, str]]:
    """Extract patient content from ``html`` using an LLM.

    Parameters
    ----------
    html:
        Raw HTML page content.
    source_url:
        URL the HTML was fetched from.
    max_chunk_chars:
        Maximum characters per LLM prompt chunk.
    """
    text = _clean_html(html)
    chunks = _chunk_text(text, max_chunk_chars)
    records: List[Dict[str, str]] = []

    for chunk in chunks:
        prompt = PROMPT_TEMPLATE.format(chunk=chunk)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        content = response["choices"][0]["message"]["content"]
        try:
            entries = json.loads(content)
        except json.JSONDecodeError:
            continue
        if isinstance(entries, dict):
            entries = [entries]
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            entry["source_url"] = source_url
            records.append(entry)

    return records
