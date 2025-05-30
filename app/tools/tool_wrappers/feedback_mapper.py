import logging
import requests
from jinja2 import Template
import yaml
from app.tools.utils.llm_helpers import chat_completion_request

logger = logging.getLogger(__name__)

class Tool:

    def run_tool(self, input_dict):
        logger.info("Running feedback mapper tool")
        feedback = input_dict["feedback_text"]
        sections = input_dict["sections"]

        # Load prompt YAML from GitHub raw URL
        prompt_url = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/app/prompts/revision_prompts.yaml"
        response = requests.get(prompt_url)
        prompts = yaml.safe_load(response.text)

        user_template = Template(prompts["feedback_mapping"]["user"])
        user_prompt = user_template.render(feedback_text=feedback, sections=sections)
        system_prompt = prompts["feedback_mapping"]["system"]

        response = chat_completion_request(system=system_prompt, user=user_prompt)

        try:
            parsed = eval(response)
            logger.info(f"Parsed feedback map: {parsed}")

            if parsed["revision_type"] not in ["rewrite", "polish", "append", "clarify", "targeted_edit"]:
                logger.warning("Unexpected revision_type. Defaulting to 'rewrite'")
                parsed["revision_type"] = "rewrite"

            return parsed
        except Exception as e:
            logger.error("Failed to parse LLM response", exc_info=e)
            return {"section_ids": [], "revision_type": "rewrite", "llm_response": response}