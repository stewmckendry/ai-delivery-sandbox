import openai
from typing import List, Dict

from .loader import load_prompt


def summarize_lab_results(results: List[Dict]) -> str:
    """Return a summary of lab results using an OpenAI model.

    Parameters
    ----------
    results: List[Dict]
        Each dict represents a lab result with keys like ``test_name``,
        ``value``, ``units``, and ``date``.
    """
    prompt = load_prompt("summarize_lab_results", {"lab_data": results})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response["choices"][0]["message"]["content"].strip()
