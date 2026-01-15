from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.bedrock_service import BedrockService
from app.services.search_service import SearchService

router = APIRouter()

class IngestRequest(BaseModel):
    text: str
    metadata: dict = {}

class IngestResponse(BaseModel):
    status: str
    chunk_count: int

@router.post("/", response_model=IngestResponse)
async def ingest_document(request: IngestRequest):
    try:
        bedrock = BedrockService()
        search = SearchService()
        
        # 1. Simple chunking (for demonstration)
        chunks = [request.text[i:i+1000] for i in range(0, len(request.text), 1000)]
        
        for chunk in chunks:
            # 2. Generate Embeddings
            vector = await bedrock.get_embeddings(chunk)
            
            # 3. Store in OpenSearch (Simplified)
            search.os_client.index(
                index="documents",
                body={
                    "text": chunk,
                    "embedding": vector,
                    "metadata": request.metadata
                }
            )
            
        return {"status": "success", "chunk_count": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
