import logging
import requests
import yaml
from jinja2 import Template
from app.tools.utils.llm_helpers import chat_completion_request

logger = logging.getLogger(__name__)

class Tool:
    def validate(self, input_dict):
        if "feedback_text" not in input_dict:
            raise ValueError("feedback_text is required")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        feedback_text = input_dict["feedback_text"]

        prompt_url = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/app/prompts/revision_prompts.yaml"
        response = requests.get(prompt_url)
        prompts = yaml.safe_load(response.text)

        template = Template(prompts["feedback_preprocess"]["user"])
        user_prompt = template.render(feedback_text=feedback_text)

        messages = [
            {"role": "system", "content": prompts["feedback_preprocess"]["system"]},
            {"role": "user", "content": user_prompt}
        ]

        response = chat_completion_request(messages, temperature=0.3)

        try:
            parsed = eval(response)
            return parsed
        except Exception as e:
            logger.warning("Failed to parse feedback preprocessing result", exc_info=e)
            return {"cleaned_text": feedback_text, "split_feedback": [feedback_text], "inferred_type": "unspecified"}