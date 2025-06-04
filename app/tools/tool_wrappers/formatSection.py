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
        section_text = data.section_text

        # Check if section_text starts with a heading (#)
        if section_text.lstrip().startswith("#"):
            logger.info(f"Section {data.section_id} starts with a heading, stripping it")
            # Find the position of the first newline after the heading
            first_newline = section_text.find('\n')
            if first_newline != -1:
                # Strip out the heading (from # to first \n)
                section_text = section_text[first_newline + 1:].lstrip()
            else:
                # If there's no newline, the whole text is a heading, so clear it
                logger.warning(f"Section {data.section_id} has no newline after heading, clearing section text")
                section_text = ""

        template_text = "<a id=\"{{ section_id }}\"></a>\n## {{ section_title }}\n\n{{ text }}"
        template = Template(template_text)
        output = template.render(
           text=section_text,
           section_title=data.section_title,
           section_id=data.section_id
        )
        return OutputSchema(formatted_section=output).dict()