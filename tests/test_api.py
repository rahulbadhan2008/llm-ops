from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_chat_endpoint_exists():
    # Just checking if the route is registered and returns 422 for empty body
    response = client.post("/api/v1/chat/")
    assert response.status_code == 422
