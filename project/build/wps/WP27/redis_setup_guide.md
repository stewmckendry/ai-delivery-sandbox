## Redis Setup Guide for Artifact Chunking

### Overview of Redis
Redis is an in-memory data store that can be used as a database, cache, and message broker. It is known for its speed, simplicity, and support for a variety of data structures such as strings, hashes, lists, and sets.

### How We're Using Redis
We use Redis to temporarily store token-chunked sections of an artifact so that they can be fetched sequentially by the GPT interface without exceeding token limits.

### Technical Design
- Chunks are stored in Redis as JSON strings.
- Each chunk set is saved under a unique key: `artifact_chunks:{session_id}:{artifact_id}`.
- Fetch operations retrieve and decode these chunks using this key.

### Fetch and Save Operations
- `SaveArtifactChunks` chunks artifact sections and stores them under the Redis key.
- `FetchArtifactChunks` retrieves the stored chunks and serves them to GPT or the frontend.

### Data Persistence
- Redis data is in-memory and is **not persisted by default**.
- In production, configure Redis with a persistence strategy (e.g., AOF or RDB).
- For now, consider Redis data to be **ephemeral** — available only for the session duration.

### Multi-User and Multi-Project Support
- Session and artifact IDs are part of the Redis key.
- This ensures isolation between users and projects, allowing concurrent access.

### Deployment Steps

#### Local Installation
1. Install Redis:
    ```bash
    brew install redis  # macOS
    sudo apt-get install redis  # Ubuntu
    ```
2. Start Redis:
    ```bash
    redis-server
    ```
3. Add to `requirements.txt`:
    ```
    redis
    ```

#### Cloud Deployment
Use [Railway](https://railway.app/) or [Redis Cloud](https://redis.com/try-free/) to provision a Redis instance.

1. Sign up and create a Redis project.
2. Copy your Redis connection string (URI).

#### Environment Variables
Add the following to your `.env` file:
```
REDIS_URL=redis://:<password>@<host>:<port>
```

On Railway, add the same to your environment variables dashboard.

#### Update Redis Client in Code
In `app/redis_client.py`, initialize:
```python
import redis
import os

redis_url = os.getenv("REDIS_URL")
redis_client = redis.Redis.from_url(redis_url)
```

### Integration with Save and Fetch Tools
Both tools use `redis_client` to store and retrieve artifact chunks.
- `SaveArtifactChunks` calls `redis_client.set(key, json_data)`
- `FetchArtifactChunks` calls `redis_client.get(key)`

### Next Steps
- Ensure Redis is running locally or available via cloud.
- Confirm environment variable `REDIS_URL` is set correctly.
- Test chunk save and fetch workflows end-to-end.

---
This guide enables robust, scalable token chunking with Redis as a session store for large artifacts.