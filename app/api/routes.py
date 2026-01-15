from fastapi import APIRouter
from app.api.endpoints import chat, ingest, memory, costs, train

router = APIRouter()

router.include_router(chat.router, prefix="/chat", tags=["Chat"])
router.include_router(ingest.router, prefix="/ingest", tags=["Ingestion"])
router.include_router(memory.router, prefix="/memory", tags=["Memory"])
router.include_router(costs.router, prefix="/costs", tags=["Cost Control"])
router.include_router(train.router, prefix="/train", tags=["Fine-Tuning"])
