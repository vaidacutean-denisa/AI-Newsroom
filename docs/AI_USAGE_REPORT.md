# Raport privind utilizarea tool-urilor AI în dezvoltarea software
## Rol: AI & Backend Developer

Acest raport documentează modul în care inteligența artificială a fost integrată în ciclul de dezvoltare a modulului de Backend (FastAPI), în orchestrarea Agenților AI (Jurnalist și Editor) și în configurarea infrastructurii (Docker), respectând cerința utilizării exhaustive a AI-ului în toate etapele proiectului.

## 🛠️ Tool-uri AI Utilizate
Gemini (Google): Utilizat ca Pair-Programmer pentru decizii de arhitectură, debugging avansat, refactoring și generarea documentației Agile, respectiv a acestui raport.

Cursor (AI IDE): Utilizat pentru generarea de cod contextual (Composer/Chat), refactoring direct în fișiere și generarea inteligentă a mesajelor de commit (funcția ✨).

GitHub Copilot: Utilizat pentru generarea titlurilor și descrierilor pentru Pull Requests.

## 🚀 Etapele de dezvoltare asistate de AI
-   1. Arhitectură, Implementare Backend și Agenți AI
    Orchestrarea Agenților: Logica de comunicare cu modelul local Ollama (Mistral) a fost dezvoltată cu asistență AI, inclusiv gestionarea prompt-urilor de sistem complexe (JOURNALIST_SYSTEM_PROMPT și EDITOR_SYSTEM_PROMPT) pentru impunerea unui format strict de output (Markdown, secțiuni delimitate).

    Servirea Interfeței: AI-ul a sugerat tranziția de la un frontend separat la un monolit deservit direct prin FastAPI (StaticFiles), eliminând astfel erorile de tip CORS.

-   2. Debugging și Refactoring
Identificarea și rezolvarea bug-urilor: Un bug critic (eroare 500) cauzat de lipsa modelului Ollama local a fost identificat și rezolvat prin generarea unui bloc de excepție specific (except HTTPError), transformând eroarea într-un mesaj user-friendly de tip 404.

-   3. Infrastructură (Dockerizare)
    Dockerizare Multi-Stage: Cursor și Gemini au fost utilizate pentru a genera un fișier Dockerfile optimizat (folosind python:3.10-slim și node:20-alpine) și un .dockerignore. AI-ul a propus o abordare eficientă de tip Multi-Stage Build pentru a compila interfața React și a o servi din containerul de Python, fără a modifica logica din main.py.

-   4. Managementul Proiectului și Source Control (Agile & Git)
    User Stories și Bug Reports: AI-ul a generat tichete standardizate pentru backlog-ul Agile, incluzând User Stories pentru Dockerizare (US16) și migrarea la React (US17), completate cu Acceptance Criteria clare. De asemenea, a redactat Bug Report-ul formal pentru eroarea 404 (Issue #12).

    Git Workflow: Toate descrierile de Pull Request-uri și mesajele de commit au fost generate folosind AI, asigurând trasabilitatea, un limbaj tehnic profesionist în limba engleză și legarea automată a PR-urilor de Issues (ex: Fixes #12).

## 🎯 Concluzie
Integrarea Agentic AI-ului în procesul de dezvoltare a transformat AI-ul dintr-un simplu generator de cod într-un partener activ de dezvoltare. A prevenit erori umane (ex: evitarea poluării repository-ului prin configurarea greșită a mediului .venv), a accelerat rezolvarea blocajelor de infrastructură (Docker) și a asigurat un standard ridicat de profesionalism în documentație și versionare.

