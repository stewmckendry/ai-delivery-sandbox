import logging
import json
from app.db.database import get_session
import tiktoken
from app.db.models.ArtifactSection import ArtifactSection
from typing import List, Dict
from pydantic import BaseModel
import requests
from collections import defaultdict
import yaml
from app.redis.redis_client import redis_client

logger = logging.getLogger(__name__)

class InputSchema(BaseModel):
    session_id: str
    artifact_id: str
    gate_id: str
    max_token: int = 1500

class ChunkedSection(BaseModel):
    section_id: str
    chunk_id: str
    text: str
    timestamp: str

class Tool:
    def __init__(self):
        self.redis_client = redis_client

    def chunk_sections(self, artifact_id: str, gate_id: str, max_token: int) -> List[Dict]:
        session = get_session()
        
        # Step 1: Get latest ArtifactSection entries by section_id
        all_entries = session.query(ArtifactSection).filter_by(
            artifact_id=artifact_id,
            gate_id=gate_id,
            status="draft"
        ).all()
        
        latest_entries = {}
        for entry in sorted(all_entries, key=lambda e: e.timestamp, reverse=True):
            if entry.section_id not in latest_entries:
                latest_entries[entry.section_id] = entry

        # Step 2: Fetch section order from GitHub reference
        yaml_url = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/project/reference/gate_reference_v2.yaml"
        response = requests.get(yaml_url)
        if response.status_code != 200:
            raise ValueError("Failed to fetch gate reference YAML from GitHub")

        gate_ref = yaml.safe_load(response.text)

        # Step 3: Locate the correct artifact and extract section order
        section_order = []
        for gate in gate_ref:
            if str(gate.get("gate_id")) == str(gate_id):
                for artifact in gate.get("artifacts", []):
                    if artifact.get("artifact_id") == artifact_id:
                        section_order = [s["section_id"] for s in artifact.get("sections", [])]
                        break
                break

        if not section_order:
            raise ValueError("No matching gate_id/artifact_id found in reference YAML")

        # Step 4: Order sections and chunk them
        tokenizer = tiktoken.get_encoding("cl100k_base")
        chunks = []

        for section_id in section_order:
            entry = latest_entries.get(section_id)
            if not entry:
                logger.warning(f"Skipping missing section_id: {section_id}")
                continue

            tokens = tokenizer.encode(entry.text)
            chunked_texts = [
                tokenizer.decode(tokens[i:i+max_token])
                for i in range(0, len(tokens), max_token)
            ]
            for idx, text_chunk in enumerate(chunked_texts):
                chunks.append(ChunkedSection(
                    section_id=entry.section_id,
                    chunk_id=f"{entry.section_id}-chunk{idx+1}",
                    text=text_chunk,
                    timestamp=entry.timestamp.isoformat()
                ).dict())

        return chunks


    def run_tool(self, input_dict):
        logger.info("[Tool] saveArtifactChunks started")
        session_id = input_dict.get("session_id")
        artifact_id = input_dict.get("artifact_id")
        gate_id = input_dict.get("gate_id")
        max_token = input_dict.get("max_token", 1500)

        if session_id is None or artifact_id is None or gate_id is None:
            raise ValueError("Missing one or more required parameters: session_id, artifact_id, gate_id")

        try:
            chunks = self.chunk_sections(artifact_id, gate_id, max_token)
            logger.info(f"Chunked {len(chunks)} sections for artifact {artifact_id} under gate {gate_id}")
            key = f"artifact_chunks:{session_id}:{artifact_id}"
            self.redis_client.set(key, json.dumps(chunks))
            logger.info(f"Saved {len(chunks)} chunks to Redis under key {key}")
            return {"status": "success", "message": f"Saved {len(chunks)} chunks."}
        except Exception as e:
            logger.error(f"Error saving chunks to Redis: {str(e)}")
            return {"status": "error", "message": str(e)}
