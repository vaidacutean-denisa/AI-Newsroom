"""
Unit tests for the custom evaluation rules in scripts/ai_evals.py.
Verifies that validations correctly pass/fail depending on input quality.
"""

from unittest.mock import patch, Mock

from scripts.ai_evals import (
    eval_markdown_and_structure,
    eval_logic_and_length,
    eval_llm_as_a_judge
)

def test_eval_markdown_and_structure_success():
    """Verify markdown validation passes with proper format."""
    valid_text = (
        "Feedback critic\n"
        "Secțiunea 1: Feedback\n"
        "Secțiunea 2: Articol final\n"
        "# Titlu Articol\n"
        "## Introducere\n"
        "Acesta este un articol corect structurat."
    )
    is_valid, msg = eval_markdown_and_structure(valid_text)
    assert is_valid is True
    assert "succes" in msg.lower()

def test_eval_markdown_and_structure_missing_headers():
    """Verify markdown validation fails when headers are missing."""
    invalid_text = (
        "Secțiunea 1: Feedback\n"
        "Secțiunea 2: Articol final\n"
        "Titlu Articol fără hashtag\n"
        "Introducere fără subtitlu"
    )
    is_valid, msg = eval_markdown_and_structure(invalid_text)
    assert is_valid is False
    assert "not contain markdown" in msg.lower()

def test_eval_markdown_and_structure_missing_sections():
    """Verify markdown validation fails when required sections are missing."""
    invalid_text = (
        "# Titlu Articol\n"
        "## Introducere\n"
        "Acesta este doar un text simplu cu markdown."
    )
    is_valid, msg = eval_markdown_and_structure(invalid_text)
    assert is_valid is False
    assert "missing" in msg.lower()

def test_eval_logic_and_length_success():
    """Verify logic validation passes when text is modified and of adequate length."""
    input_text = "Acesta este un draft scurt de test."
    output_text = "Acesta este un articol final mult mai elaborat, rescris de editor, cu text nou adăugat."
    is_valid, msg = eval_logic_and_length(input_text, output_text)
    assert is_valid is True
    assert "successful" in msg.lower()

def test_eval_logic_and_length_identical():
    """Verify logic validation fails when output is identical to input."""
    text = "Acesta este un draft de test de lungime corespunzătoare."
    is_valid, msg = eval_logic_and_length(text, text)
    assert is_valid is False
    assert "identical to input" in msg.lower()

def test_eval_logic_and_length_too_short():
    """Verify logic validation fails when output text is too short."""
    input_text = "Acesta este un draft scurt de test."
    output_text = "Scurt."
    is_valid, msg = eval_logic_and_length(input_text, output_text)
    assert is_valid is False
    assert "too short" in msg.lower()

@patch("scripts.ai_evals.requests.post")
def test_eval_llm_as_a_judge_success(mock_post):
    """Verify G-Eval judge returns high scores on good generated article."""
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "response": '{"coherence_score": 5, "relevance_score": 4, "reasoning": "Articolul este foarte bun."}'
    }
    mock_post.return_value = mock_resp

    scores = eval_llm_as_a_judge("Draft", "Articol final", is_ci=False)
    assert scores["coherence_score"] == 5
    assert scores["relevance_score"] == 4
    assert "foarte bun" in scores["reasoning"]

@patch("scripts.ai_evals.requests.post")
def test_eval_llm_as_a_judge_fail_coherence(mock_post):
    """Verify G-Eval judge correctly yields low coherence score when text is incoherent."""
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "response": '{"coherence_score": 2, "relevance_score": 4, "reasoning": "Textul are probleme grave de fluență."}'
    }
    mock_post.return_value = mock_resp

    scores = eval_llm_as_a_judge("Draft", "Incoherent output", is_ci=False)
    assert scores["coherence_score"] == 2
    assert scores["relevance_score"] == 4
    assert scores["coherence_score"] < 3  # Low coherence score (<3 threshold)

@patch("scripts.ai_evals.requests.post")
def test_eval_llm_as_a_judge_fail_relevance(mock_post):
    """Verify G-Eval judge yields low relevance score when output diverges from draft topic."""
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "response": '{"coherence_score": 4, "relevance_score": 1, "reasoning": "Articolul vorbește despre alt subiect."}'
    }
    mock_post.return_value = mock_resp

    scores = eval_llm_as_a_judge("Draft about AI", "Article about cooking", is_ci=False)
    assert scores["coherence_score"] == 4
    assert scores["relevance_score"] == 1
    assert scores["relevance_score"] < 3  # Low relevance score (<3 threshold)
