from typing import Dict
from pydantic import BaseModel
from jinja2 import Template
import os
import yaml

TEMPLATE_DIR = "project/reference/artifact_templates/"

class InputSchema(BaseModel):
    section_id: str
    section_text: str
    template_file: str  # relative to TEMPLATE_DIR

class OutputSchema(BaseModel):
    formatted_section: str

class Tool:
    def validate(self, input_dict: Dict) -> InputSchema:
        return InputSchema(**input_dict)

    def run_tool(self, input_dict: Dict) -> Dict:
        data = self.validate(input_dict)
        template_path = os.path.join(TEMPLATE_DIR, data.template_file)

        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(template_path, "r") as f:
            template_str = f.read()
        template = Template(template_str)

        output = template.render(text=data.section_text, section_id=data.section_id)
        return OutputSchema(formatted_section=output).dict()