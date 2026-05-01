"""FastAPI service for local Ollama interactions."""

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from requests.exceptions import ConnectionError as RequestsConnectionError, Timeout

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"
JOURNALIST_SYSTEM_PROMPT = (
    "Ești un 'Content Creator' și un jurnalist de top. Sarcina ta este să primești "
    "un subiect și să generezi un draft de articol detaliat și coerent.\n"
    "Reguli stricte:\n"
    "1. Textul final trebuie să aibă minim 300 de cuvinte.\n"
    "2. Trebuie să acoperi cel puțin 3 idei sau perspective distincte și relevante "
    "despre subiect.\n"
    "3. Rămâi strict la tema dată."
    "4. TREBUIE SĂ SCRII DRAFTUL EXCLUSIV ÎN LIMBA ROMÂNĂ. Nu folosi limba engleză."
)
INVALID_PROMPT_MESSAGE = (
    "Te rugăm să introduci un subiect valid pentru a putea scrie articolul."
)


class PromptRequest(BaseModel):
    """Request payload for LLM prompt endpoint."""

    prompt: str


def _validate_prompt(prompt: str) -> str:
    """Validate prompt content and return cleaned value."""

    clean_prompt = prompt.strip()
    if len(clean_prompt) < 3:
        raise HTTPException(status_code=400, detail=INVALID_PROMPT_MESSAGE)
    return clean_prompt


def _call_ollama(payload: dict):
    """Call Ollama API and normalize error handling."""

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()

    except RequestsConnectionError as exc:
        raise HTTPException(
            status_code=503, detail="Eroare: Serviciul Ollama nu este pornit local."
        ) from exc

    except Timeout as exc:
        raise HTTPException(
            status_code=504, detail="Eroare: Timeout la conectarea cu modelul Ollama."
        ) from exc

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/")
def root():
    """Return service health status."""

    return {"message": "AI-Newsroom API is running"}


@app.post("/ask")
def ask_llm(request: PromptRequest):
    """Send prompt to local Ollama model and return response."""

    payload = {"model": MODEL_NAME, "prompt": request.prompt, "stream": False}
    return _call_ollama(payload)


@app.post("/journalist/draft")
def create_journalist_draft(request: PromptRequest):
    """Generate article draft using journalist system prompt."""

    clean_prompt = _validate_prompt(request.prompt)
    payload = {
        "model": MODEL_NAME,
        "system": JOURNALIST_SYSTEM_PROMPT,
        "prompt": clean_prompt,
        "stream": False,
    }
    return _call_ollama(payload)
