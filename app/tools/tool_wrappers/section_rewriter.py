import logging
import requests
from jinja2 import Template
import yaml
from app.tools.utils.llm_helpers import chat_completion_request
from app.tools.tool_wrappers.revision_checker import Tool as RevisionChecker

logger = logging.getLogger(__name__)

class Tool:
    def validate(self, input_dict):
        required = ["section_id", "feedback", "revision_type", "current_text"]
        for r in required:
            if r not in input_dict:
                raise ValueError(f"Missing required input: {r}")

    def run_tool(self, input_dict):
        self.validate(input_dict)

        section_id = input_dict["section_id"]
        feedback = input_dict["feedback"]
        revision_type = input_dict["revision_type"]
        current_text = input_dict["current_text"]

        # Load prompt template from GitHub
        prompt_url = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/app/prompts/revision_prompts.yaml"
        response = requests.get(prompt_url)
        prompts = yaml.safe_load(response.text)
        prompt_template = Template(prompts["section_rewrite"][revision_type])

        user_prompt = prompt_template.render(section_id=section_id, feedback=feedback, current_text=current_text)

        messages = [
            {"role": "system", "content": "You are a policy analyst editing a government document section."},
            {"role": "user", "content": user_prompt}
        ]

        response = chat_completion_request(messages, temperature=0.4)
        draft = response.strip()

        # Run revision checker on the result
        checker = RevisionChecker()
        check_result = checker.run_tool({
            "original_text": current_text,
            "revised_text": draft,
            "revision_type": revision_type
        })

        return {
            "section_id": section_id,
            "draft": draft,
            "prompt_used": user_prompt,
            "revision_check": check_result
        }