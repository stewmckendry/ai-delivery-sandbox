import json
import logging
import tiktoken
from typing import List, Dict
from app.db.models.ArtifactSection import ArtifactSection
from app.tools.base_tool import BaseTool
from app.tools.schemas.saveArtifactChunks import InputSchema, ChunkedSection
from app.db.session import get_session
from app.redis_client import redis_client

logger = logging.getLogger(__name__)

class SaveArtifactChunks(BaseTool):
    def __init__(self):
        self.redis_client = redis_client

    def chunk_sections(self, artifact_id: str, gate_id: str, project_id: str, session_id: str, max_token: int) -> List[Dict]:
        session = get_session()
        entries = session.query(ArtifactSection).filter_by(
            artifact_id=artifact_id,
            gate_id=gate_id,
            project_id=project_id,
            session_id=session_id
        ).all()

        tokenizer = tiktoken.get_encoding("cl100k_base")
        chunks = []

        for e in entries:
            tokens = tokenizer.encode(e.text)
            chunked_texts = [
                tokenizer.decode(tokens[i:i+max_token])
                for i in range(0, len(tokens), max_token)
            ]
            for idx, text_chunk in enumerate(chunked_texts):
                chunks.append(ChunkedSection(
                    section_id=e.section_id,
                    chunk_id=f"{e.section_id}-chunk{idx+1}",
                    text=text_chunk,
                    timestamp=e.timestamp.isoformat()
                ).dict())

        return chunks

    def run_tool(self, input_dict):
        session_id = input_dict.get("session_id")
        artifact_id = input_dict.get("artifact_id")
        gate_id = input_dict.get("gate_id")
        project_id = input_dict.get("project_id")
        max_token = input_dict.get("max_token", 1500)

        if not all([session_id, artifact_id, gate_id, project_id]):
            raise ValueError("Missing one or more required parameters: session_id, artifact_id, gate_id, project_id")

        try:
            chunks = self.chunk_sections(artifact_id, gate_id, project_id, session_id, max_token)
            key = f"artifact_chunks:{session_id}:{artifact_id}"
            self.redis_client.set(key, json.dumps(chunks))
            logger.info(f"Saved {len(chunks)} chunks to Redis under key {key}")
            return {"status": "success", "message": f"Saved {len(chunks)} chunks."}
        except Exception as e:
            logger.error(f"Error saving chunks to Redis: {str(e)}")
            return {"status": "error", "message": str(e)}
