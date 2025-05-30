from typing import Dict
from pydantic import BaseModel, parse_obj_as
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

class InputSchema(BaseModel):
    title: str
    document_body: str
    version: str
    artifact_id: str
    gate_id: str
    sections: list[dict]  # List of dicts with keys: section_id and title

class OutputSchema(BaseModel):
    final_markdown: str

class Tool:
    def run_tool(self, input_dict: Dict) -> Dict:
        logger.info("Running finalizeDocument tool")
        data = parse_obj_as(InputSchema, input_dict)
        header = f"# {data.title}\n\n**Version:** {data.version}  \\\n**Artifact ID:** {data.artifact_id}  \\\n**Gate ID:** {data.gate_id}  \\\n**Generated On:** {datetime.utcnow().isoformat()}\n\n---\n"

        toc = "## Table of Contents\n"
        for section in data.sections:
            title = section.get("title", "")
            section_id = section.get("section_id", "")
            toc += f"- [{title}](#{section_id})\n"
        toc += "\n"

        final_md = header + toc + data.document_body
        return OutputSchema(final_markdown=final_md).dict()