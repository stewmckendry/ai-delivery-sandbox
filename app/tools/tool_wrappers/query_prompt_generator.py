import os
from jinja2 import Template
from app.tools.utils.llm_helpers import get_prompt

class Tool:
    def validate(self, input_dict):
        if "project_profile" not in input_dict:
            raise ValueError("Missing required field: project_profile")
        if "memory" not in input_dict:
            raise ValueError("Missing required field: memory")

    def run_tool(self, input_dict):
        self.validate(input_dict)

        profile = input_dict["project_profile"]
        memory = input_dict["memory"]

        profile_summary = "\n".join([f"{k}: {v}" for k, v in profile.items()])
        memory_context = "\n".join([f"- {entry.get('input_summary', '')}: {entry.get('full_input_path', '')}" for entry in memory])

        prompt_cfg = get_prompt("generate_section_prompts.yaml", "search_query_generation")
        user_prompt_template = Template(prompt_cfg["user"])
        user_prompt = user_prompt_template.render(profile_summary=profile_summary, memory_context=memory_context)

        return {"query": user_prompt, "system": prompt_cfg["system"]}
