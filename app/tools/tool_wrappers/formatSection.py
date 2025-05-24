from typing import Dict
from pydantic import BaseModel
from jinja2 import Template
import requests

class InputSchema(BaseModel):
    section_id: str
    section_text: str
    template_url: str  # GitHub raw URL to template

class OutputSchema(BaseModel):
    formatted_section: str

class Tool:
    def validate(self, input_dict: Dict) -> InputSchema:
        return InputSchema(**input_dict)

    def run_tool(self, input_dict: Dict) -> Dict:
        data = self.validate(input_dict)
        response = requests.get(data.template_url)
        if response.status_code != 200:
            raise FileNotFoundError(f"Template not found at: {data.template_url}")

        template = Template(response.text)
        output = template.render(text=data.section_text, section_id=data.section_id)
        return OutputSchema(formatted_section=output).dict()