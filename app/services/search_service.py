from opensearchpy import OpenSearch
from neo4j import GraphDatabase
from app.core.config import settings

class SearchService:
    def __init__(self):
        self.os_client = OpenSearch(
            hosts=[{'host': settings.OPENSEARCH_HOST, 'port': settings.OPENSEARCH_PORT}],
            http_auth=(settings.OPENSEARCH_USER, settings.OPENSEARCH_PASS),
            use_ssl=True,
            verify_certs=False,
            ssl_show_warn=False
        )
        self.neo4j_driver = GraphDatabase.driver(
            settings.NEO4J_URI, 
            auth=(settings.NEO4J_USER, settings.NEO4J_PASS)
        )

    async def hybrid_search(self, query: str, vector: list[float], limit: int = 5):
        # 1. OpenSearch BM25 + Vector Search
        os_query = {
            "size": limit,
            "query": {
                "hybrid": {
                    "queries": [
                        {"match": {"text": query}},
                        {"knn": {"embedding": {"vector": vector, "k": limit}}}
                    ]
                }
            }
        }
        os_results = self.os_client.search(index="documents", body=os_query)
        
        # 2. Neo4j Graph Search (for context)
        kg_context = self._query_neo4j(query)
        
        return {
            "vector_results": os_results['hits']['hits'],
            "graph_context": kg_context
        }

    def _query_neo4j(self, query: str):
        # Simplified Cypher query for demonstration
        with self.neo4j_driver.session() as session:
            result = session.run(
                "MATCH (n)-[r]->(m) WHERE n.name CONTAINS $query RETURN n, r, m LIMIT 5",
                query=query
            )
            return [record.data() for record in result]

    async def close(self):
        self.neo4j_driver.close()
