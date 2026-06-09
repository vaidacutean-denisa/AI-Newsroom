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


## Rol: DevOps & Pipeline Automation Engineer

Acest raport documentează modul în care inteligența artificială a fost integrată în configurarea și optimizarea infrastructurii de Continuous Integration și Continuous Delivery (CI/CD), în corectarea erorilor de arhitectură din mediile izolate și în sincronizarea modulelor Full-Stack, asigurând conformitatea cu cerințele privind utilizarea exhaustivă a componentelor AI în ciclul de viață al proiectului.

## 🛠️ Tool-uri AI Utilizate
* **Gemini (Google):** Utilizat ca arhitect DevOps virtual și expert în depanare (Pair-Programmer) pentru diagnosticarea erorilor de rulare din GitHub Actions, generarea corecțiilor de rețea/rute și redactarea raportului academic de față.
* **itHub Copilot:** Utilizate pentru optimizarea sintaxei fișierelor de configurare YAML, autocompletarea căilor relative în scripturile de testare și generarea automată a mesajelor tehnice de commit aferente procesului de integrare.

## 🚀 Etapele de dezvoltare asistate de AI

### 1. Proiectarea și Extinderea Pipeline-ului CI/CD
* **Automatizarea Fluxurilor (CI & CD):** Logica inițială de Continuous Integration a fost extinsă cu asistența AI prin adăugarea unui job secundar, automatizat, destinat Continuous Delivery (CD). AI-ul a implementat reguli condiționale stricte (`needs: build-and-test` și structuri de tip `if`), asigurându-se că generarea imaginii de producție are loc exclusiv în urma trecerii tuturor testelor unitare și doar la detectarea unui eveniment de tip `push` pe branch-urile stabile (`main`, `develop`).
* **Containerizare Automatizată:** Pasul de CD a fost configurat cu ajutorul AI-ului pentru a utiliza acțiuni standardizate (`docker/setup-buildx-action@v3`), orchestrând asamblarea automată a containerului de backend (`ai-newsroom-backend:latest`) în mod steril pe runner-ul de GitHub Actions.

### 2. Debugging Avansat și Rezolvarea Eroilor de Context (Environment Debugging)
* **Remedierea Erorilor de Structură (`ENOENT`):** În faza de asamblare a frontend-ului, pipeline-ul genera o eroare cauzată de absența fișierului `package.json` în rădăcina proiectului. Prin analizarea structurii directoarelor, AI-ul a identificat că ecosistemul React era izolat în subdirectorul `frontend-react/`. Soluția generată de AI a constat în injectarea directivei `working-directory` în interiorul pașilor definiți pentru Node.js, redirecționând contextual execuția comenzilor `npm install` și `npm run build`.
  
### 3. Soluționarea Conflictelor Arhitecturale Full-Stack (Pytest 404 Resolution)
* **Izolarea Mediului de Testare:** Ulterior compilării frontend-ului, testele unitare executate prin `pytest` raportau erori de tipul `404 Not Found` la interogarea rutei `/`. AI-ul a diagnosticat conflictul arhitectural: montarea fișierelor statice (`app.mount("/", StaticFiles(...))`) suprascria comportamentul rutei de backend în cadrul runner-ului virtual.
* **Refactoring Asistat de AI:** La recomandarea AI-ului, s-a optat pentru decuplarea testelor automate de starea fișierelor statice. AI-ul a generat un nou endpoint dedicat stării sistemului (`@app.get("/health")`) în `main.py` și a ghidat refactorizarea completă a aserțiunilor din suitele de testare `tests/test_llm_integration.py` și `tests/test_qa_pipeline.py`. Această abordare a restabilit validarea corectă a codurilor de stare `200 OK` sub formă de răspunsuri JSON structurate.

### 4. Managementul Git Workflow și Livrarea Codului
* **Ghidare Contextuală CLI:** În faza de Source Control, la apariția erorii `fatal: pathspec`, AI-ul a interpretat corect poziția curentă a utilizatorului în structura de directoare (`.github/workflows/`) și a oferit instrucțiunile de navigare relativă pentru adăugarea și stocarea corectă a fișierelor modificate.

## 🎯 Concluzie
Integrarea instrumentelor de inteligență artificială în zona de DevOps a demonstrat că AI-ul poate acționa ca un inginer de sistem capabil să asigure coerența între module software eterogene. Prin intermediul asistenței AI, au fost eliminate blocajele de mapare a directoarelor și conflictele de rutare din aplicația monolit, livrându-se un flux de integrare și containerizare complet automatizat, stabil și aliniat la standardele riguroase din industrie.
