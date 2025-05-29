import redis
import os

redis_url = os.getenv("REDIS_URL")
redis_client = redis.Redis.from_url(redis_url)
