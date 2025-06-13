import openai
from typing import List, Dict, Any


def chat_completion(messages: List[Dict[str, str]], *, model: str = "gpt-3.5-turbo", **kwargs: Any) -> str:
    """Return the assistant message content from an OpenAI chat completion."""
    response = openai.chat.completions.create(model=model, messages=messages, **kwargs)
    return response.choices[0].message.content.strip()
