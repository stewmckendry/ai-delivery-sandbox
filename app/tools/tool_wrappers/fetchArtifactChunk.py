import logging
from app.db.artifact_chunks import get_artifact_chunk

logger = logging.getLogger(__name__)

class FetchArtifactChunk:
    def run_tool(self, input_dict):
        artifact_id = input_dict.get("artifact_id")
        session_id = input_dict.get("session_id")
        chunk_id = input_dict.get("chunk_id", 0)

        if not artifact_id or not session_id:
            raise ValueError("Missing required parameters: artifact_id or session_id")

        logger.info(f"Fetching chunk {chunk_id} for artifact {artifact_id} and session {session_id}")

        chunk = get_artifact_chunk(session_id=session_id, artifact_id=artifact_id, chunk_id=chunk_id)

        return {
            "chunk_id": chunk_id,
            "text": chunk.get("text", ""),
            "is_last": chunk.get("is_last", False)
        }