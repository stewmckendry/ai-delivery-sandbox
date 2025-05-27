import logging
import requests
from difflib import SequenceMatcher
import yaml
from jinja2 import Template
from app.tools.utils.llm_helpers import chat_completion_request

logger = logging.getLogger(__name__)

class Tool:
    def validate(self, input_dict):
        required = ["original_text", "revised_text", "revision_type"]
        for r in required:
            if r not in input_dict:
                raise ValueError(f"Missing required input: {r}")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        orig = input_dict["original_text"]
        revised = input_dict["revised_text"]
        revision_type = input_dict["revision_type"]

        matcher = SequenceMatcher(None, orig.strip(), revised.strip())
        similarity = matcher.ratio()
        change_ratio = 1 - similarity

        flags = []
        if revision_type in ["polish", "targeted_edit"] and change_ratio > 0.3:
            flags.append("high_diff_for_minor_edit")

        # Load LLM validation prompt from GitHub
        prompt_url = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/app/prompts/revision_prompts.yaml"
        response = requests.get(prompt_url)
        prompts = yaml.safe_load(response.text)
        template = Template(prompts["revision_check"]["user"])

        user_prompt = template.render(revision_type=revision_type, original_text=orig, revised_text=revised)
        messages = [
            {"role": "system", "content": prompts["revision_check"]["system"]},
            {"role": "user", "content": user_prompt}
        ]

        response = chat_completion_request(messages, temperature=0.2)

        return {
            "change_ratio": round(change_ratio, 3),
            "flags": flags,
            "llm_verdict": response
        }