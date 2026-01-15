from app.services.bedrock_service import BedrockService
from app.services.search_service import SearchService
from app.services.memory_service import MemoryService
import logging

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.bedrock = BedrockService()
        self.search = SearchService()
        self.memory = MemoryService()

    async def process_query(self, query: str, user_id: str, session_id: str):
        # 1. Fetch Memory/Context
        history = await self.memory.get_memory(user_id, session_id)
        
        # 2. Hybrid Search (Vector + Graph)
        vector = await self.bedrock.get_embeddings(query)
        search_results = await self.search.hybrid_search(query, vector)
        
        # 3. Augment Prompt
        context = self._build_context(search_results, history)
        prompt = f"Context: {context}\n\nQuestion: {query}"
        
        # 4. Generate Response
        answer = await self.bedrock.generate_response(
            prompt=prompt,
            system_prompt="You are a helpful assistant. Use the provided context to answer questions."
        )
        
        # 5. Save Interaction to Memory
        await self.memory.save_memory(user_id, session_id, {
            "query": query,
            "answer": answer,
            "timestamp": "now"
        })
        
        return {
            "answer": answer,
            "sources": [res['_source'].get('title', 'Unknown') for res in search_results['vector_results']]
        }

    def _build_context(self, search_results, history):
        ctx = "Search Results:\n"
        for res in search_results['vector_results']:
            ctx += f"- {res['_source']['text']}\n"
        
        ctx += "\nGraph Context:\n"
        for res in search_results['graph_context']:
            ctx += f"- {res}\n"
            
        return ctx
