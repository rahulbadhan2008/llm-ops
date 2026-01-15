from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.rag_service import RAGService

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    user_id: str
    session_id: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, rag_service: RAGService = Depends(RAGService)):
    response = await rag_service.process_query(
        query=request.query,
        user_id=request.user_id,
        session_id=request.session_id
    )
    return response
