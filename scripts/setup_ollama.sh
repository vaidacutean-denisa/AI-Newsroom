#!/bin/bash
echo "Verificare Ollama..."
ollama --version || echo "Instalează Ollama de pe https://ollama.com"
ollama pull mistral
