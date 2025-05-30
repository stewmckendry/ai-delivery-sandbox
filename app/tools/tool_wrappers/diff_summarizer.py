import logging
from jinja2 import Template
from app.tools.utils.llm_helpers import chat_completion_request, get_prompt

logger = logging.getLogger(__name__)

class Tool:
    def run_tool(self, input_dict):
        logger.info("Running diff_summarizer tool")

        original = input_dict.get("original_text", "")
        revised = input_dict.get("new_text", "")

        if not original or not revised:
            raise ValueError("Missing original or revised text")

        prompts = get_prompt("revision_prompts.yaml", "diff_summary")
        user_prompt = Template(prompts["user"]).render(original=original, revised=revised)
        system_prompt = prompts["system"]

        response = chat_completion_request(system=system_prompt, user=user_prompt, temperature=0)
        return {"diff_summary": response}
