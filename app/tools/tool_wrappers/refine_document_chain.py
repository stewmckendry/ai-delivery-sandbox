from typing import Dict, List
from pydantic import BaseModel, parse_obj_as
from jinja2 import Template
import yaml
import os
import logging
import re
from app.tools.utils.llm_helpers import chat_completion_request
from app.tools.utils.section_helpers import get_token_count

logger = logging.getLogger(__name__)

class InputSchema(BaseModel):
    document_body: str
    title: str = None
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
        self.chunk_token_target = 3500

    def split_document(self, document_body: str) -> List[str]:
        # Splits on section headers (## ...), groups into token-bound chunks
        sections = re.split(r"(## .+)", document_body)
        sections = [s.strip() for s in sections if s.strip()]

        chunks, current, current_tokens = [], [], 0
        for part in sections:
            current.append(part)
            current_tokens += get_token_count(part)
            if current_tokens >= self.chunk_token_target:
                chunks.append("\n\n".join(current))
                current, current_tokens = [], 0
        if current:
            chunks.append("\n\n".join(current))
        return chunks

    def run_tool(self, input_dict: Dict) -> Dict:
        data = parse_obj_as(InputSchema, input_dict)

        system_prompt = self.prompts["system"]
        title = data.title
        document_body = data.document_body

        if get_token_count(document_body) <= self.token_limit:
            user_prompt = Template(self.prompts["user"]).render(title=title, document_body=document_body)
            response = chat_completion_request(system=system_prompt.strip(), user=user_prompt.strip())
            return OutputSchema(refined_body=response.strip(), skipped=False).dict()

        # Token limit exceeded, apply chunking
        chunks = self.split_document(document_body)
        stitched_output = []
        summary = ""

        for i, chunk in enumerate(chunks):
            chunk_prompt = Template(self.prompts["user"]).render(title=title, document_body=summary + chunk)
            response = chat_completion_request(system=system_prompt.strip(), user=chunk_prompt.strip())
            stitched_output.append(response.strip())
            summary += f"\n[Summary of Section {i+1}]:\n" + response.strip()[:300]

        return OutputSchema(refined_body="\n\n".join(stitched_output), skipped=False).dict()