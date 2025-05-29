import logging
from redis import Redis

logger = logging.getLogger(__name__)

class FetchArtifactChunk:
    def __init__(self):
        self.redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)

    def run_tool(self, input_dict):
        session_id = input_dict.get("session_id")
        chunk_id = input_dict.get("chunk_id")

        if not session_id or not chunk_id:
            raise ValueError("Missing session_id or chunk_id in input_dict.")

        redis_key = f"{session_id}:{chunk_id}"
        chunk_data = redis_client.get(redis_key)

        if chunk_data is None:
            raise ValueError(f"No chunk found for key: {redis_key}")

        return json.loads(chunk_data)
