from fastapi import APIRouter

from .rag import router as rag_router
from .upload import router as upload_router

router = APIRouter()
router.include_router(rag_router)
router.include_router(upload_router)
