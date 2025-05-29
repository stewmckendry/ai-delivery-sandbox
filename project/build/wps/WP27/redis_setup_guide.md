## Redis Setup Guide for Artifact Chunking
### Overview of Redis

Redis is an in-memory data store used as a database, cache, and message broker. It is valued for its speed, simplicity, and support for data structures like strings, hashes, lists, and sets.

### How We're Using Redis

Redis temporarily stores token-chunked sections of artifacts, allowing sequential fetching by the GPT interface without exceeding token limits.

### Technical Design

- Chunks are stored as JSON strings in Redis.
- Each chunk set uses a unique key: `artifact_chunks:{session_id}:{artifact_id}`.
- Fetch operations retrieve and decode chunks using this key.

### Fetch and Save Operations

- `SaveArtifactChunks` splits artifact sections into chunks and stores them under the Redis key.
- `FetchArtifactChunks` retrieves stored chunks for GPT or the frontend.

### Data Persistence

- Redis data is in-memory and **not persisted by default**.
- For production, configure persistence (AOF or RDB).
- For now, treat Redis data as **ephemeral**—available only during the session.

### Multi-User and Multi-Project Support

- Session and artifact IDs are included in the Redis key.
- This ensures isolation between users and projects, supporting concurrent access.

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

Provision a Redis instance using [Railway](https://railway.app/) or [Redis Cloud](https://redis.com/try-free/):

1. Sign up and create a Redis project.
2. Copy your Redis connection string (URI).

#### Environment Variables

Add to your `.env` file:
```
REDIS_URL=redis://:<password>@<host>:<port>
```
On Railway, add the same variable in the environment dashboard.

#### Update Redis Client in Code

In `app/redis_client.py`:
```python
import redis
import os

redis_url = os.getenv("REDIS_URL")
redis_client = redis.Redis.from_url(redis_url)
```

### Integration with Save and Fetch Tools

Both tools use `redis_client` to store and retrieve artifact chunks:
- `SaveArtifactChunks`: `redis_client.set(key, json_data)`
- `FetchArtifactChunks`: `redis_client.get(key)`

### Next Steps

- Ensure Redis is running locally or available via cloud.
- Confirm `REDIS_URL` is set correctly.
- Test chunk save and fetch workflows end-to-end.

---

This guide enables robust, scalable token chunking with Redis as a session store for large artifacts.

---

#### Addendum: Redis Deployment Steps

**Step-by-Step: Add Redis Plugin to Your Railway Project**

1. Go to your Railway project.
2. Click the **+ Create** button in the top-right.
3. In the pop-up, choose **Database** and select **Redis**.
4. Wait for Railway to provision a Redis instance.

**Find Your Redis Connection String**

1. Go to the new Redis plugin tab in your project.
2. Find the environment variable it exposes (usually `REDIS_URL`).
3. Copy the value (e.g., `redis://default:<password>@<host>:<port>`).

**Add to Environment Variables**

1. In Railway, open the Variables tab of your main service.
2. Add a new variable:
    - Name: `REDIS_URL`
    - Value: Paste the connection string
3. Do the same locally in your `.env` file for local testing.