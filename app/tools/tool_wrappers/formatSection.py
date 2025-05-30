from typing import Dict
from pydantic import BaseModel, parse_obj_as
from jinja2 import Template
import logging
logger = logging.getLogger(__name__)

class InputSchema(BaseModel):
    section_id: str
    section_text: str
    section_title: str
    artifact_id: str

class OutputSchema(BaseModel):
    formatted_section: str

class Tool:
    def run_tool(self, input_dict: Dict) -> Dict:
        logger.info("Running formatSection tool")
        data = parse_obj_as(InputSchema, input_dict)
        template_text = "<a id=\"{{ section_id }}\"></a>\n## {{ section_title }}\n\n{{ text }}"
        template = Template(template_text)
        output = template.render(
           text=data.section_text,
           section_title=data.section_title,
           section_id=data.section_id
        )
        return OutputSchema(formatted_section=output).dict()