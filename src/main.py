import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from requests.exceptions import ConnectionError

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"


class PromptRequest(BaseModel):
    prompt: str


@app.get("/")
def root():
    return {"message": "AI-Newsroom API is running"}


@app.post("/ask")
def ask_llm(request: PromptRequest):
    payload = {
        "model": MODEL_NAME,
        "prompt": request.prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()

    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Eroare: Serviciul Ollama nu este pornit local."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
