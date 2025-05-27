from typing import Dict
from pydantic import BaseModel, parse_obj_as
from jinja2 import Template
import yaml, os
from app.tools.utils.llm_helpers import call_llm_chat

class QueryPromptInput(BaseModel):
    section_title: str
    section_text: str
    project_profile: str
    artifact_purpose: str
    context_summary: str = ""

class QueryPromptOutput(BaseModel):
    questions: str

class Tool:
    def __init__(self):
        with open("app/prompts/generate_section_prompts.yaml", "r") as f:
            self.prompts = yaml.safe_load(f)["query_prompt"]

    def run_tool(self, input_dict: Dict) -> Dict:
        data = parse_obj_as(QueryPromptInput, input_dict)
        user_prompt = Template(self.prompts["user"]).render(**data.dict())
        response = call_llm_chat(system=self.prompts["system"], user=user_prompt, model="gpt-4", temperature=0.5)
        return QueryPromptOutput(questions=response.strip()).dict()