from app.db.database import get_session
from app.db.models.ArtifactSection import ArtifactSection
from pydantic import BaseModel
from typing import List, Dict
import tiktoken
from datetime import datetime

class InputSchema(BaseModel):
    artifact_id: str
    gate_id: str
    max_token: int

class ChunkedSection(BaseModel):
    section_id: str
    chunk_id: str
    text: str
    timestamp: str

class Tool:
    def run_tool(self, input_dict) -> List[Dict]:
        validated = InputSchema(**input_dict)
        session = get_session()

        entries = session.query(ArtifactSection).filter_by(
            artifact_id=validated.artifact_id,
            gate_id=validated.gate_id,
            status="draft"
        ).all()

        tokenizer = tiktoken.get_encoding("cl100k_base")
        chunks = []

        for e in entries:
            tokens = tokenizer.encode(e.text)
            chunked_texts = [
                tokenizer.decode(tokens[i:i+validated.max_token])
                for i in range(0, len(tokens), validated.max_token)
            ]
            for idx, text_chunk in enumerate(chunked_texts):
                chunks.append(ChunkedSection(
                    section_id=e.section_id,
                    chunk_id=f"{e.section_id}-chunk{idx+1}",
                    text=text_chunk,
                    timestamp=e.timestamp.isoformat()
                ).dict())

        return chunks