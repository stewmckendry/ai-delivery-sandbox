import logging
import requests
from jinja2 import Template
import yaml
from app.tools.utils.llm_helpers import chat_completion_request

logger = logging.getLogger(__name__)

class Tool:
    def validate(self, input_dict):
        if "feedback_text" not in input_dict:
            raise ValueError("feedback_text is required")
        if "sections" not in input_dict:
            raise ValueError("sections list is required")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        feedback = input_dict["feedback_text"]
        sections = input_dict["sections"]

        # Load prompt YAML from GitHub raw URL
        prompt_url = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/app/prompts/revision_prompts.yaml"
        response = requests.get(prompt_url)
        prompts = yaml.safe_load(response.text)

        user_template = Template(prompts["feedback_mapping"]["user"])
        user_prompt = user_template.render(feedback_text=feedback, sections=sections)
        system_prompt = prompts["feedback_mapping"]["system"]

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = chat_completion_request(messages, temperature=0.2)

        try:
            parsed = eval(response)
            logger.info(f"Parsed feedback map: {parsed}")
            return parsed
        except Exception as e:
            logger.error("Failed to parse LLM response", exc_info=e)
            return {"section_ids": [], "revision_type": "rewrite", "llm_response": response}