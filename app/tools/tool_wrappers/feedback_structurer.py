import logging
from app.tools.utils.llm_helpers import chat_completion_request
from jinja2 import Template
import yaml
import requests

logger = logging.getLogger(__name__)

class Tool:
    def run_tool(self, input_dict):
        logger.info("Running unified feedback structurer tool")
        feedback_text = input_dict["feedback_text"]
        sections = input_dict["sections"]

        prompt_url = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/app/prompts/revision_prompts.yaml"
        response = requests.get(prompt_url)
        prompts = yaml.safe_load(response.text)

        user_template = Template(prompts["feedback_structuring"]["user"])
        user_prompt = user_template.render(feedback_text=feedback_text, sections=sections)
        system_prompt = prompts["feedback_structuring"]["system"]

        response = chat_completion_request(system=system_prompt, user=user_prompt)

        try:
            parsed = eval(response)
            logger.info("Parsed feedback structure: %s", parsed)
            return parsed
        except Exception as e:
            logger.warning("Failed to parse structuring result", exc_info=e)
            return {"mapped_feedback": []}