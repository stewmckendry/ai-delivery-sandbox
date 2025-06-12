from fastapi import APIRouter

from .rag import router as rag_router

router = APIRouter()
router.include_router(rag_router)
