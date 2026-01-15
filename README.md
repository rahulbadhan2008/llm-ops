# LLM Ops Project: End-to-End Hybrid RAG Pipeline

A production-ready implementation of a Hybrid RAG system using **AWS Bedrock**, **OpenSearch**, **Neo4j**, and **FastAPI**.

## 🌐 End-to-End Workflow

This project integrates several complex layers to ensure high accuracy and low latency.

### 1. User Interaction (The Chat Flow)
1.  **Incoming Query**: User sends a question through the FastAPI endpoint.
2.  **State Management**: System checks **Redis** for active 8-hour sessions. If expired, it pulls recent history from **DynamoDB**.
3.  **Hybrid Search**: 
    - **Vector Search**: Semantic lookup in OpenSearch.
    - **Graph Search**: Detailed entity relationship lookup in Neo4j.
4.  **Generation**: **Claude 3 (via Bedrock)** processes the context and query to produce a grounded response.
5.  **Persistence**: The interaction is saved to **S3** for long-term auditing and future fine-tuning.

### 2. DevOps & CI/CD Lifecycle
- **Push**: Code is pushed to Git.
- **Verify**: `pytest` runs unit tests and performance benchmarks (`p50` latency).
- **Build**: Docker image is built and pushed to **Amazon ECR**.
- **Deploy**: **ECS** performs a rolling update.
- **Rollback**: If the new version fails health checks, ECS automatically reverts to the previous stable state.

---

## 🏗 System Architecture
For a deep dive into schemas, network diagrams, and detailed logic, see **[architecture.md](architecture.md)**.

## 📄 API Documentation
For detailed information on every endpoint (Chat, Ingest, Memory, Costs, Train), see **[api_documentation.md](api_documentation.md)**.

## 🚀 Getting Started

### Prerequisites
- AWS Account with Bedrock access.
- Terraform installed (for infrastructure setup).
- Docker & Docker Compose.

### Local Development
1.  Clone the repo and `cp .env.example .env`.
2.  Run the orchestration script: `./run.sh` (Starts services, runs tests, and benchmarks).
3.  Access Swagger UI at `http://localhost:8000/docs`.

### Running Tests Separately
```bash
pytest tests/
```

### Deploying Infrastructure
```bash
cd infrastructure/terraform
terraform init
terraform apply
```

## 🛠 Features
- **Hybrid RAG**: BM25 + Vector + Graph search.
- **Three-Tier Memory**: Caching layer, 7-day short-term, and perpetual long-term storage.
- **Production Infrastructure**: Full Terraform support for ECS, RDS, and OpenSearch.
- **Benchmarking**: Automated P50/P90/P95 latency tracking.
- **Cost Management**: Per-user token tracking and AWS budget alerts.

## 📈 Monitoring & Logging
- **Logs**: Streamed to CloudWatch Log Groups.
- **Metrics**: Custom latency and token usage metrics in CloudWatch.

## 📜 License
MIT
