from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    """Basic health check endpoint."""
    return {"status": "ok"}

# Placeholder: include routers from app/api when available
try:
    from app.api import router as api_router  # type: ignore
    app.include_router(api_router)
except Exception:
    pass
