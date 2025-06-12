import openai
from typing import List, Dict


def summarize_blocks(blocks: List[Dict[str, str]]) -> str:
    """Return a natural-language summary of text blocks using OpenAI.

    Parameters
    ----------
    blocks: List[Dict[str, str]]
        Sequence of dictionaries each containing a ``"text"`` field.

    Returns
    -------
    str
        Concise summary of the provided text.
    """

    system_prompt = (
        "Summarize the following content in a way that highlights key details "
        "clearly. Assume the text may include medical records, summaries, or "
        "observations. Output a concise, readable summary."
    )

    combined_text = "\n".join(block.get("text", "") for block in blocks)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": combined_text},
        ],
    )
    return response["choices"][0]["message"]["content"].strip()
