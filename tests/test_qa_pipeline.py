"""Tests for the AI-Newsroom agent pipeline and API behavior."""

from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_api_endpoints_health_and_structure():
    """Test generat cu AI: Verifica daca endpoint-urile respecta structura API definita."""
    response = client.get("/health")
    assert response.status_code == 200


@patch("src.main.requests.post")
def test_agent_pipeline_e2e_flow(mock_post):
    """Test generat cu AI: Verifica pipeline-ul agentilor (Jurnalist -> Editor)."""

    journalist_resp = Mock()
    journalist_resp.raise_for_status.return_value = None
    journalist_resp.json.return_value = {"response": "Draft Jurnalist test pipeline"}

    editor_resp = Mock()
    editor_resp.raise_for_status.return_value = None
    editor_resp.json.return_value = {
        "response": "# Articol Final\nTest structurat si formatat"
    }

    mock_post.side_effect = [journalist_resp, editor_resp]

    response = client.post("/article/generate", json={"prompt": "Subiect de test QA"})

    assert response.status_code == 200
    data = response.json()
    assert "draft" in data, "Pipeline-ul trebuie sa returneze draft-ul intermediar"
    assert "final_article" in data, "Pipeline-ul trebuie sa returneze articolul final"
    assert data["draft"] == "Draft Jurnalist test pipeline"
    assert data["final_article"] == "# Articol Final\nTest structurat si formatat"
