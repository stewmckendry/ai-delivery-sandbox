from typing import Dict
from pydantic import BaseModel, parse_obj_as
from jinja2 import Template
import yaml
import os
import logging
from app.tools.utils.llm_helpers import call_llm
from app.tools.utils.section_helpers import get_token_count

logger = logging.getLogger(__name__)

class InputSchema(BaseModel):
    document_body: str
    title: str = "Policy Document"
    project_id: str = None

class OutputSchema(BaseModel):
    refined_body: str
    skipped: bool

class Tool:
    def __init__(self):
        prompt_path = os.path.join("app", "prompts", "refine_document_prompts.yaml")
        with open(prompt_path, "r") as f:
            self.prompts = yaml.safe_load(f)["refine_document"]

        self.token_limit = 7000

    def run_tool(self, input_dict: Dict) -> Dict:
        data = parse_obj_as(InputSchema, input_dict)

        if get_token_count(data.document_body) > self.token_limit:
            logger.warning("Document exceeds token limit – skipping refinement.")
            return OutputSchema(refined_body=data.document_body, skipped=True).dict()

        system_prompt = self.prompts["system"]
        user_prompt = Template(self.prompts["user"]).render(
            title=data.title, document_body=data.document_body
        )

        response = call_llm(
            system=system_prompt.strip(),
            user=user_prompt.strip(),
            temperature=0.3,
            model="gpt-4"
        )

        return OutputSchema(refined_body=response.strip(), skipped=False).dict()