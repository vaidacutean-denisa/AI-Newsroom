"""Integration tests for LLM API endpoints."""

from unittest.mock import patch
from requests.exceptions import ConnectionError as RequestsConnectionError, Timeout
from fastapi.testclient import TestClient
from src.main import INVALID_PROMPT_MESSAGE, JOURNALIST_SYSTEM_PROMPT, app

client = TestClient(app)


def test_health_check():
    """Validate health endpoint response."""

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "AI-Newsroom API is running"}


@patch("src.main.requests.post")
def test_success_response(mock_post):
    """Validate successful /ask response flow."""

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"response": "Salut!"}

    response = client.post("/ask", json={"prompt": "test"})

    assert response.status_code == 200
    assert "response" in response.json()


@patch("src.main.requests.post")
def test_error_handling_ollama_offline(mock_post):
    """Validate offline Ollama error mapping."""

    mock_post.side_effect = RequestsConnectionError()

    response = client.post("/ask", json={"prompt": "test"})

    assert response.status_code == 503
    assert response.json()["detail"] == "Eroare: Serviciul Ollama nu este pornit local."


@patch("src.main.requests.post")
def test_error_handling_ollama_timeout(mock_post):
    """Validate timeout error mapping."""

    mock_post.side_effect = Timeout()

    response = client.post("/ask", json={"prompt": "test"})

    assert response.status_code == 504
    assert (
        response.json()["detail"] == "Eroare: Timeout la conectarea cu modelul Ollama."
    )


def test_journalist_draft_invalid_input():
    """Validate friendly 400 for empty or too-short journalist prompt."""

    response = client.post("/journalist/draft", json={"prompt": "  "})

    assert response.status_code == 400
    assert response.json()["detail"] == INVALID_PROMPT_MESSAGE


@patch("src.main.requests.post")
def test_journalist_draft_success_payload_contains_system_prompt(mock_post):
    """Validate journalist payload includes required system prompt."""

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"response": "Draft articol"}

    response = client.post(
        "/journalist/draft", json={"prompt": "Inteligența artificială"}
    )

    assert response.status_code == 200
    assert response.json()["response"] == "Draft articol"
    _, kwargs = mock_post.call_args
    payload = kwargs["json"]
    assert payload["model"] == "mistral"
    assert payload["prompt"] == "Inteligența artificială"
    assert payload["stream"] is False
    assert payload["system"] == JOURNALIST_SYSTEM_PROMPT
