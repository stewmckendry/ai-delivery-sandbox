from typing import Dict
from pydantic import BaseModel, parse_obj_as
from jinja2 import Template
import yaml, os
from app.tools.utils.llm_helpers import call_llm_chat

class SectionRefineInput(BaseModel):
    section_text: str
    prior_summary: str = ""

class SectionRefineOutput(BaseModel):
    polished_text: str

class Tool:
    def __init__(self):
        with open("app/prompts/generate_section_prompts.yaml", "r") as f:
            self.prompts = yaml.safe_load(f)["section_refinement"]

    def run_tool(self, input_dict: Dict) -> Dict:
        data = parse_obj_as(SectionRefineInput, input_dict)
        user_prompt = Template(self.prompts["polish"]).render(**data.dict())
        response = call_llm_chat(system="You are a government document editor.", user=user_prompt, model="gpt-4", temperature=0.3)
        return SectionRefineOutput(polished_text=response.strip()).dict()