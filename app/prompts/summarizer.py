import openai
from typing import List, Dict


SYSTEM_PROMPT = (
    "Summarize the following content in a way that highlights key details clearly. "
    "Assume the text may include medical records, summaries, or observations. "
    "Output a concise, readable summary."
)


def summarize_blocks(blocks: List[Dict[str, str]]) -> str:
    """Return a summary of text blocks using an OpenAI model."""

    combined = "\n\n".join(block.get("text", "") for block in blocks)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": combined},
        ],
    )
    return response["choices"][0]["message"]["content"].strip()


# Backwards compatibility
summarize_lab_results = summarize_blocks
