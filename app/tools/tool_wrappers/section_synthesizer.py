from typing import Dict
from pydantic import BaseModel, parse_obj_as
import yaml, os
from jinja2 import Template
from app.tools.utils.llm_helpers import call_llm_chat

class SectionDraftInput(BaseModel):
    section_title: str
    artifact_name: str
    gate_name: str
    project_profile: str
    user_inputs: str
    artifact_purpose: str
    section_intents: list
    context_summary: str = ""

class SectionDraftOutput(BaseModel):
    section_text: str

class Tool:
    def __init__(self):
        prompt_path = os.path.join("app", "prompts", "generate_section_prompts.yaml")
        with open(prompt_path, "r") as f:
            self.prompts = yaml.safe_load(f)["section_synthesis"]

    def run_tool(self, input_dict: Dict) -> Dict:
        data = parse_obj_as(SectionDraftInput, input_dict)
        user_prompt = Template(self.prompts["user"]).render(**data.dict())
        system_prompt = self.prompts["system"]
        response = call_llm_chat(system=system_prompt, user=user_prompt, model="gpt-4", temperature=0.3)
        return SectionDraftOutput(section_text=response.strip()).dict()