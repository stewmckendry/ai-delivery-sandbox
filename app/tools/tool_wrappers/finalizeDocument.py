from typing import Dict
from pydantic import BaseModel
from datetime import datetime

class InputSchema(BaseModel):
    title: str
    document_body: str
    version: str
    artifact_id: str
    gate_id: str

class OutputSchema(BaseModel):
    final_markdown: str

class Tool:
    def validate(self, input_dict: Dict) -> InputSchema:
        return InputSchema(**input_dict)

    def run_tool(self, input_dict: Dict) -> Dict:
        data = self.validate(input_dict)
        header = f"# {data.title}\n\n**Version:** {data.version}  \\\n**Artifact ID:** {data.artifact_id}  \\\n**Gate ID:** {data.gate_id}  \\\n**Generated On:** {datetime.utcnow().isoformat()}\n\n---\n"

        toc = "## Table of Contents\n" + "\n".join([
            f"- [{line[2:]}](#{line[2:].lower().replace(' ', '-')})"
            for line in data.document_body.splitlines() if line.startswith("## ")
        ]) + "\n\n"

        final_md = header + toc + data.document_body
        return OutputSchema(final_markdown=final_md).dict()