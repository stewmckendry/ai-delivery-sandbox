import redis
import os
from dotenv import load_dotenv

load_dotenv()
redis_url = os.getenv("REDIS_URL")

if not redis_url:
	raise ValueError("REDIS_URL environment variable is not set")
redis_client = redis.Redis.from_url(redis_url)
