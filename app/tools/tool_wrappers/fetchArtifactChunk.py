import logging
import json
from app.redis.redis_client import redis_client


logger = logging.getLogger(__name__)

class Tool:
    def __init__(self):
        self.redis_client = redis_client

    def run_tool(self, input_dict):
        session_id = input_dict.get("session_id")
        artifact_id = input_dict.get("artifact_id")
        chunk_id = input_dict.get("chunk_id")

        if not session_id or not chunk_id or not artifact_id:
            raise ValueError("Missing session_id, artifact_id, or chunk_id in input_dict.")

        redis_key = f"artifact_chunks:{session_id}:{artifact_id}"
        all_chunks_raw = redis_client.get(redis_key)

        if all_chunks_raw is None:
            raise ValueError(f"No chunks found for key: {redis_key}")

        all_chunks = json.loads(all_chunks_raw)

        for chunk in all_chunks:
            if chunk.get("chunk_id") == chunk_id:
                return chunk

        raise ValueError(f"Chunk ID '{chunk_id}' not found in artifact '{artifact_id}' for session '{session_id}'.")

