from unittest.mock import patch
from requests.exceptions import ConnectionError
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "AI-Newsroom API is running"}


@patch("main.requests.post")
def test_success_response(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "response": "Salut!"
    }

    response = client.post("/ask", json={"prompt": "test"})

    assert response.status_code == 200
    assert "response" in response.json()


@patch("main.requests.post")
def test_error_handling_ollama_offline(mock_post):
    mock_post.side_effect = ConnectionError()

    response = client.post("/ask", json={"prompt": "test"})

    assert response.status_code == 503
    assert response.json()["detail"] == "Eroare: Serviciul Ollama nu este pornit local."
