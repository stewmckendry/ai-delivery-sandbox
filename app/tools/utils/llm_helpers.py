import os
import yaml
from openai import OpenAI


def chat_completion_request(system, user, temperature=0.7, model="gpt-4"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content.strip()


def get_prompt(prompt_file, block):
    import requests
    import tempfile
    base_url = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/app/prompts/"
    prompt_url = f"{base_url}{prompt_file}"

    response = requests.get(prompt_url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch prompt file: {prompt_url}")

    prompt_yaml = yaml.safe_load(response.text)
    if block not in prompt_yaml:
        raise ValueError(f"Block '{block}' not found in prompt file {prompt_file}")

    return prompt_yaml[block]