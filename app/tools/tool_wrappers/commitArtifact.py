from typing import Dict
from pydantic import BaseModel
import os
from datetime import datetime

class InputSchema(BaseModel):
    final_markdown: str
    artifact_id: str
    gate_id: str
    version: str
    title: str

class OutputSchema(BaseModel):
    local_path: str
    drive_url: str  # placeholder

class Tool:
    def validate(self, input_dict: Dict) -> InputSchema:
        return InputSchema(**input_dict)

    def run_tool(self, input_dict: Dict) -> Dict:
        data = self.validate(input_dict)
        filename = f"{data.artifact_id}_gate{data.gate_id}_v{data.version}_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.md"
        out_path = os.path.join("output", filename)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        with open(out_path, "w") as f:
            f.write(data.final_markdown)

        # TODO: Replace with Google Drive storage in WP20
        return OutputSchema(
            local_path=out_path,
            drive_url="TODO: Replace with Google Drive link in WP20"
        ).dict()