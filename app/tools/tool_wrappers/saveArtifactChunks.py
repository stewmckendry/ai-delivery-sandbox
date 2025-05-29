import logging
from redis import Redis
import json

logger = logging.getLogger(__name__)

class SaveArtifactChunks:
    def __init__(self):
        self.redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)

    def run_tool(self, input_dict):
        session_id = input_dict.get("session_id")
        artifact_id = input_dict.get("artifact_id")
        chunks = input_dict.get("chunks")

        if not all([session_id, artifact_id, chunks]):
            raise ValueError("Missing one or more required parameters: session_id, artifact_id, chunks")

        key = f"artifact_chunks:{session_id}:{artifact_id}"
        try:
            self.redis_client.set(key, json.dumps(chunks))
            logger.info(f"Saved {len(chunks)} chunks to Redis under key {key}")
            return {"status": "success", "message": f"Saved {len(chunks)} chunks."}
        except Exception as e:
            logger.error(f"Error saving chunks to Redis: {str(e)}")
            return {"status": "error", "message": str(e)}