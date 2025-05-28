import os
from dotenv import load_dotenv
from jinja2 import Template
from app.tools.utils.llm_helpers import chat_completion_request, get_prompt
import logging
logger = logging.getLogger(__name__)

load_dotenv()

class Tool:
    def validate(self, input_dict):
        if "raw_draft" not in input_dict:
            raise ValueError("Missing required field: raw_draft")

    def run_tool(self, input_dict):
        logger.info("[Tool] section_refiner started")
        self.validate(input_dict)
        raw_draft = input_dict.get("raw_draft")

        prompt_templates = get_prompt("generate_section_prompts.yaml", "section_refinement")
        system_prompt_template = Template(prompt_templates["system"])
        user_prompt_template = Template(prompt_templates["user"])

        system_prompt = system_prompt_template.render()
        user_prompt = user_prompt_template.render(raw_draft=raw_draft)

        refined = chat_completion_request(system_prompt, user_prompt, temperature=0.5)
        logger.info(f"[Tool] section_refiner output: {refined[:100]}...")
        return {"raw_draft": refined, "prompt_used": user_prompt}
