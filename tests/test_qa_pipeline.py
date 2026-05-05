from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from src.main import app

client = TestClient(app)

def test_api_endpoints_health_and_structure():
    """Test generat cu AI: Verifica daca endpoint-urile respecta structura API definita."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
