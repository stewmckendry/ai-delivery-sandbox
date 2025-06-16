from fastapi import APIRouter

from .rag import router as rag_router
from .upload import router as upload_router
from .etl import router as etl_router
from .status import router as status_router

router = APIRouter()
router.include_router(rag_router)
router.include_router(upload_router)
router.include_router(etl_router)
router.include_router(status_router)
