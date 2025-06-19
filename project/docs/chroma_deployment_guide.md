# Chroma Vector Store Deployment

This guide describes how to host a ChromaDB instance on Railway and connect it to the FastAPI server.

## Deploy Chroma
1. Create a new Railway project.
2. Add the provided `Dockerfile` and `docker-compose.yaml` from this repo.
3. Expose port `8000` in the service.
4. Set environment variables:
   ```env
   CHROMA_HTTP_PORT=8000
   CHROMA_SERVER_AUTH_TOKEN=<secure_token>
   ```
   Generate a random UUID for `<secure_token>` and store it in Railway secrets.

## Configure FastAPI Server
In the AI Copilot project, set:
```env
USE_REMOTE_CHROMA=true
CHROMA_SERVER_HOST=https://<your-chroma-subdomain>.up.railway.app
CHROMA_TOKEN=<secure_token>
```
The host value comes from the Railway URL after deploying Chroma. Use the same token value as above.

## Verify Connectivity
1. Upload health records and run the ETL pipeline so they are indexed.
2. Call `/ask_vector` with a question. If records were indexed, the answer should reference the retrieved context.
3. Ensure results only include records for the current `session_key`.
