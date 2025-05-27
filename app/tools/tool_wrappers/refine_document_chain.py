import logging
from app.tools.base_tool import Tool
from app.tools.utils.llm_helpers import call_llm
from app.tools.utils.section_helpers import get_token_count
from jinja2 import Template
import yaml
import os

logger = logging.getLogger(__name__)

class RefineDocumentChain(Tool):
    def __init__(self):
        super().__init__()
        self.name = "refineDocumentChain"
        self.description = "Refines and polishes a document for tone, structure, and clarity"
        self.token_limit = 7000

        prompt_path = os.path.join("app", "prompts", "refine_document_prompts.yaml")
        with open(prompt_path, "r") as f:
            self.prompts = yaml.safe_load(f)["refine_document"]

    def run_tool(self, inputs):
        document_body = inputs["document_body"]
        title = inputs.get("title", "Policy Document")

        if get_token_count(document_body) > self.token_limit:
            logger.warning("Document exceeds token limit – skipping refinement.")
            return {"refined_body": document_body, "skipped": True}

        system_prompt = self.prompts["system"]
        user_prompt = Template(self.prompts["user"]).render(
            title=title, document_body=document_body
        )

        response = call_llm(
            system=system_prompt.strip(),
            user=user_prompt.strip(),
            temperature=0.3,
            model="gpt-4"
        )

        return {"refined_body": response.strip(), "skipped": False}

    def validate(self, inputs):
        assert "document_body" in inputs, "Missing document_body input"