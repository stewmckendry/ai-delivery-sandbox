import logging
import json
from app.redis.redis_client import redis_client

logger = logging.getLogger(__name__)

class Tool:
    def run_tool(self, input_dict):
        artifact_id = input_dict["artifact_id"]
        session_id = input_dict["session_id"]
        project_id = input_dict["project_id"]
        section_id = input_dict.get("section_id")

        base_key = f"revise:{project_id}:{artifact_id}:{session_id}"  # Optional suffix: :{section_id}
        keys = [f"{base_key}:{section_id}"] if section_id else redis_client.keys(f"{base_key}:*")

        results = []
        for key in keys:
            try:
                val = redis_client.get(key)
                if not val:
                    continue
                data = json.loads(val)
                results.append({
                    "section_id": key.decode().split(":")[-1] if isinstance(key, bytes) else key.split(":")[-1],
                    "revised": data.get("revised"),
                    "diff_summary": data.get("diff_summary")
                })
            except Exception as e:
                logger.warning(f"Failed to parse Redis key {key}: {e}")
                continue

        return {"sections": results, "total": len(results)}