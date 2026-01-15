import time
import statistics
import asyncio
from app.services.rag_service import RAGService
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

async def run_benchmark(num_requests: int = 50):
    latencies = []
    print(f"Starting benchmark with {num_requests} requests...")
    
    for i in range(num_requests):
        start_time = time.time()
        
        # Simulating a chat request
        response = client.post("/api/v1/chat/", json={
            "query": "What is LLM Ops?",
            "user_id": "test_user",
            "session_id": f"session_{i}"
        })
        
        end_time = time.time()
        latency = (end_time - start_time) * 1000 # in ms
        
        if response.status_code == 200:
            latencies.append(latency)
        else:
            print(f"Request {i} failed with status {response.status_code}")

    if not latencies:
        print("All requests failed.")
        return

    p50 = statistics.median(latencies)
    p90 = statistics.quantiles(latencies, n=10)[8]
    p95 = statistics.quantiles(latencies, n=20)[18]
    avg = sum(latencies) / len(latencies)

    print("\n--- Benchmark Results ---")
    print(f"Average Latency: {avg:.2f} ms")
    print(f"P50 Latency:     {p50:.2f} ms")
    print(f"P90 Latency:     {p90:.2f} ms")
    print(f"P95 Latency:     {p95:.2f} ms")
    print(f"Success Rate:    {(len(latencies)/num_requests)*100:.2f}%")
    print("-------------------------\n")

if __name__ == "__main__":
    # Note: Requires AWS credentials and running services for accurate RAG timing
    # For now, this acts as a template for production benchmarking
    asyncio.run(run_benchmark(10))
