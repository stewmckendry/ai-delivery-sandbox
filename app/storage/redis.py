from __future__ import annotations

import os
from dotenv import load_dotenv
import redis

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

_redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True,
)


def set_key(key: str, value: str, expire: int | None = None) -> bool:
    """Set ``key`` to ``value`` with optional expiration in seconds."""
    return bool(_redis_client.set(name=key, value=value, ex=expire))


def get_key(key: str) -> str | None:
    """Retrieve the value for ``key`` if present."""
    return _redis_client.get(name=key)


def delete_key(key: str) -> int:
    """Delete ``key`` from Redis, returning the number of keys removed."""
    return _redis_client.delete(key)


def is_connected() -> bool:
    """Check if the Redis client can connect."""
    try:
        return _redis_client.ping()
    except redis.RedisError:
        return False


if __name__ == "__main__":
    example_key = "demo"
    set_key(example_key, "hello world", expire=60)
    print("Value:", get_key(example_key))
    delete_key(example_key)
    print("After delete:", get_key(example_key))
