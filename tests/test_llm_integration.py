"""Integration tests for LLM API endpoints."""

from unittest.mock import Mock, patch
from requests.exceptions import ConnectionError as RequestsConnectionError, Timeout
from fastapi.testclient import TestClient
from src.main import (
    EDITOR_SYSTEM_PROMPT,
    INVALID_DRAFT_MESSAGE,
    INVALID_LLM_OUTPUT_MESSAGE,
    INVALID_PROMPT_MESSAGE,
    JOURNALIST_SYSTEM_PROMPT,
    app,
)

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


def test_editor_review_invalid_input():
    """Validate friendly 400 for empty or too-short editor draft."""

    response = client.post("/editor/review", json={"draft": " "})

    assert response.status_code == 400
    assert response.json()["detail"] == INVALID_DRAFT_MESSAGE


@patch("src.main.requests.post")
def test_editor_review_success_payload_contains_system_prompt(mock_post):
    """Validate editor payload includes required system prompt."""

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"response": "Articol revizuit"}

    response = client.post("/editor/review", json={"draft": "Draft inițial articol"})

    assert response.status_code == 200
    assert response.json()["response"] == "Articol revizuit"
    _, kwargs = mock_post.call_args
    payload = kwargs["json"]
    assert payload["model"] == "mistral"
    assert payload["prompt"] == "Draft inițial articol"
    assert payload["stream"] is False
    assert payload["system"] == EDITOR_SYSTEM_PROMPT


@patch("src.main.requests.post")
def test_workflow_generate_success(mock_post):
    """Validate orchestrated workflow returns draft and final article."""

    journalist_response = Mock()
    journalist_response.raise_for_status.return_value = None
    journalist_response.json.return_value = {"response": "Draft generat de jurnalist"}

    editor_response = Mock()
    editor_response.raise_for_status.return_value = None
    editor_response.json.return_value = {"response": "Articol final îmbunătățit"}

    mock_post.side_effect = [journalist_response, editor_response]

    response = client.post("/article/generate", json={"prompt": "Energie regenerabilă"})

    assert response.status_code == 200
    assert response.json()["draft"] == "Draft generat de jurnalist"
    assert response.json()["final_article"] == "Articol final îmbunătățit"
    assert mock_post.call_count == 2


@patch("src.main.logger.error")
@patch("src.main.requests.post")
def test_workflow_generate_error_logging(mock_post, mock_logger_error):
    """Validate workflow handles timeout and logs editor step error."""

    journalist_response = Mock()
    journalist_response.raise_for_status.return_value = None
    journalist_response.json.return_value = {"response": "Draft valid pentru editor"}

    mock_post.side_effect = [journalist_response, Timeout()]

    response = client.post("/article/generate", json={"prompt": "Educație digitală"})

    assert response.status_code == 504
    mock_logger_error.assert_called_once()
    assert "Editor step" in mock_logger_error.call_args[0][0]


@patch("src.main.requests.post")
def test_workflow_generate_invalid_journalist_output_returns_server_error(mock_post):
    """Validate invalid journalist output is surfaced as server-side failure."""

    journalist_response = Mock()
    journalist_response.raise_for_status.return_value = None
    journalist_response.json.return_value = {"response": " "}
    mock_post.side_effect = [journalist_response]

    response = client.post("/article/generate", json={"prompt": "Smart cities"})

    assert response.status_code == 502
    assert response.json()["detail"] == INVALID_LLM_OUTPUT_MESSAGE
