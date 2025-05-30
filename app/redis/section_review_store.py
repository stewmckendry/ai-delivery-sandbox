import json
from typing import Dict, List
from app.redis.redis_client import redis_client


def _key(session_id: str, project_id: str, artifact_id: str) -> str:
    return f"section_review:{project_id}:{artifact_id}:{session_id}"


def store_section(session_id: str, project_id: str, artifact_id: str, section_id: str, section_data: Dict):
    key = _key(session_id, project_id, artifact_id)
    redis_client.hset(key, section_id, json.dumps(section_data))


def fetch_review_section(session_id: str, project_id: str, artifact_id: str, section_id: str) -> Dict:
    key = _key(session_id, project_id, artifact_id)
    data = redis_client.hget(key, section_id)
    return json.loads(data) if data else None


def get_all_sections(session_id: str, project_id: str, artifact_id: str) -> List[Dict]:
    key = _key(session_id, project_id, artifact_id)
    all_data = redis_client.hgetall(key)
    return [{"section_id": k.decode(), **json.loads(v)} for k, v in all_data.items()]


def delete_section(session_id: str, project_id: str, artifact_id: str, section_id: str):
    key = _key(session_id, project_id, artifact_id)
    redis_client.hdel(key, section_id)


def clear_all_sections(session_id: str, project_id: str, artifact_id: str):
    key = _key(session_id, project_id, artifact_id)
    redis_client.delete(key)

def list_review_sections(session_id: str, project_id: str, artifact_id: str) -> List[str]:
    key = _key(session_id, project_id, artifact_id)
    return [k.decode() for k in redis_client.hkeys(key)]
