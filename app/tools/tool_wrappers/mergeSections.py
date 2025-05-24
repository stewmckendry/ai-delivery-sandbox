from typing import List, Dict
from pydantic import BaseModel

class InputSchema(BaseModel):
    sections: List[str]  # List of pre-formatted section strings

class OutputSchema(BaseModel):
    document_body: str

class Tool:
    def validate(self, input_dict: Dict) -> InputSchema:
        return InputSchema(**input_dict)

    def run_tool(self, input_dict: Dict) -> Dict:
        data = self.validate(input_dict)
        merged = "\n\n".join(data.sections)
        return OutputSchema(document_body=merged).dict()