from typing import List, Dict
from pydantic import BaseModel, parse_obj_as

class InputSchema(BaseModel):
    sections: List[str]  # List of pre-formatted section strings

class OutputSchema(BaseModel):
    document_body: str

class Tool:
    def run_tool(self, input_dict: Dict) -> Dict:
        data = parse_obj_as(InputSchema, input_dict)
        merged = "\n\n".join(data.sections)
        return OutputSchema(document_body=merged).dict()