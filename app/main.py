from fastapi import FastAPI
from fastapi import APIRouter


from .api.rag import router as rag_router
from .api.upload import router as upload_router
from .api.etl import router as etl_router
from .api.status import router as status_router
from .api.export import router as export_router

app = FastAPI()
router = APIRouter()
router.include_router(rag_router)
router.include_router(upload_router)
router.include_router(etl_router)
router.include_router(status_router)
router.include_router(export_router)
app.include_router(router)


@app.get("/")
async def root() -> dict[str, str]:
    """Basic health check endpoint."""
    return {"status": "ok"}

# Placeholder: include routers from app/api when available
try:
    router.include_router(rag_router)
    router.include_router(upload_router)
    router.include_router(etl_router)
    router.include_router(status_router)
    router.include_router(export_router)
except Exception:
    pass
