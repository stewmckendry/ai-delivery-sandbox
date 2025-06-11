# AI Delivery Sandbox

This repository contains a collection of FastAPI tools and automation scripts used in the AI Delivery System. The project includes tool wrappers, chain implementations, and extensive documentation under `project/docs`.

## Required Environment Variables

Before running the application or tests, set the following variables (usually via a `.env` file or your shell):

- `DATABASE_URL` – SQLAlchemy connection string for the logging database.
- `REDIS_URL` – connection URL for Redis used by certain toolchains.
- `SERPAPI_KEY` – API key for the SerpAPI web search service.
- **Google Drive credentials** used by the drive tools:
  - `GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON_PATH` – path to a service account JSON file.
  - `GOOGLE_DRIVE_SCOPES` – OAuth scopes (e.g. `https://www.googleapis.com/auth/drive.file`).
  - Optional `GOOGLE_DRIVE_CLIENT_EMAIL` and `GOOGLE_DRIVE_PRIVATE_KEY` if not using a JSON file.

## Running the FastAPI App

1. Install dependencies (preferably in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`. The generated OpenAPI specification lives in [openapi.json](openapi.json).

Alternatively you can run the stack with Docker:
```bash
docker-compose up --build
```

## Running Tests

Export the repository root on `PYTHONPATH` and invoke `pytest`:

```bash
export PYTHONPATH=$PWD
pytest
```

Sample tests live under `project/test`. They cover toolchains such as those in `WP24`.

## Additional Documentation

Onboarding and process documentation is located under [`project/docs`](project/docs). Useful entry points:

- [Human Lead Onboarding Guide](project/docs/onboarding_guide.md)
- [Non‑Technical Onboarding Guide](project/docs/onboarding_guide_simple.md)

## License

This repository is for demonstration and experimentation purposes.
