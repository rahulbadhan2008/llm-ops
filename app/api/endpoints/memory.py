from fastapi import APIRouter
from app.services.memory_service import MemoryService

router = APIRouter()

@router.get("/{user_id}")
async def get_user_memory(user_id: str):
    memory_service = MemoryService()
    history = memory_service._get_dynamo_memory(user_id)
    return {"user_id": user_id, "history": history}
