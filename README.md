# AI-Newsroom – Generator de Conținut Bazat pe Agenți AI

## 📌 Descriere

Acest proiect propune o aplicație web pentru generarea asistată de conținut, construită pe baza unui **workflow multi-agent AI**, în care mai multe entități inteligente colaborează pentru a produce un rezultat final de calitate.

Spre deosebire de abordările clasice bazate pe un singur model de limbaj, sistemul implementează o **separare explicită a responsabilităților** între doi agenți AI specializați:

- ✍️ **Agentul Jurnalist** – responsabil pentru explorarea subiectului și generarea unui draft inițial  
- 🧾 **Agentul Editor Șef** – responsabil pentru evaluarea critică, restructurarea și rafinarea conținutului  

Această arhitectură reflectă un proces real de redactare, în care conținutul este iterativ îmbunătățit prin colaborare între roluri distincte.

---

## 🎯 Obiective

Proiectul urmărește atingerea mai multor obiective:

- demonstrarea utilizării **sistemelor multi-agent AI** într-un context aplicat  
- integrarea **tool-urilor de inteligență artificială în toate etapele dezvoltării software**  
- crearea unui sistem care oferă **transparență asupra procesului de generare**, nu doar asupra rezultatului final  
- explorarea limitărilor modelelor de limbaj (ex: halucinații) și atenuarea acestora prin post-procesare  

---

## ⚙️ Fluxul de Execuție

Procesul de generare este orchestrat de backend și se desfășoară în mai multe etape:

1. Utilizatorul introduce un subiect  
2. **Agentul Jurnalist** generează un draft inițial, fără constrângeri stricte de structură  
3. Draftul este transmis către **Agentul Editor**, care:
   - analizează coerența și relevanța conținutului  
   - identifică redundanțe și ambiguități  
   - restructurează informația în secțiuni logice  
   - produce o versiune finală formatată în Markdown  
4. Aplicația expune utilizatorului:
   - starea fiecărui agent  
   - rezultatele intermediare  
   - forma finală a articolului  

---

## 🧩 Arhitectură

Sistemul este organizat modular, pentru a separa responsabilitățile și a facilita extensibilitatea:

- **Frontend Layer** – interfață pentru input și vizualizarea procesului  
- **Backend Layer** – orchestration logic și gestionarea fluxului de date  
- **Agent Layer** – implementarea agenților și a logicii de interacțiune dintre aceștia  
- **Model Layer** – modele de limbaj rulate local (ex: Ollama, LM Studio)  

Această structură permite înlocuirea sau extinderea ușoară a agenților sau a modelelor utilizate.

---

## 🤖 Design-ul Agenților

### 📰 Agentul Jurnalist
- orientat spre generare creativă  
- produce conținut detaliat, dar posibil imperfect  
- nu impune constrângeri stricte de structură  

### ✏️ Agentul Editor Șef
- orientat spre analiză critică și rafinare  
- aplică reguli de coerență și structurare  
- transformă output-ul brut într-un rezultat final profesionist  

Interacțiunea dintre agenți ilustrează un model simplificat de **colaborare asincronă între agenți AI**.

---

## 🔍 Funcționalități

- generare de articole pornind de la un subiect liber  
- workflow multi-agent transparent  
- vizualizare în timp real a etapelor de procesare  
- afișare draft intermediar + rezultat final  
- export al conținutului generat  

---

## 🧪 Testare și Evaluare

Pentru a asigura consistența sistemului, proiectul include:

- teste automate pentru componentele backend  
- **AI Evals** pentru validarea comportamentului agenților  
- verificarea respectării structurii și formatării output-ului  

---

## 👥 Contribuția Echipei

Proiectul a fost realizat în echipă, fiecare membru având responsabilități clar definite, aliniate cu diferite etape ale procesului de dezvoltare software:

### 🛠️ DevOps & Git Master
- configurarea repository-ului și a structurii de proiect  
- gestionarea branch-urilor și a workflow-ului Git  
- implementarea pipeline-ului CI/CD (GitHub Actions)  
- integrarea și organizarea tool-urilor AI utilizate în dezvoltare  

---

### 🤖 AI & Backend Developer
- integrarea modelelor de limbaj locale (ex: Ollama, LM Studio)  
- proiectarea și implementarea agenților AI  
- definirea și rafinarea prompturilor (prompt engineering)  
- dezvoltarea logicii de orchestrare între agenți  

---

### 🧪 QA & AI Evals Engineer
- dezvoltarea testelor automate pentru backend  
- implementarea scripturilor de evaluare (AI Evals)  
- verificarea consistenței și calității output-ului agenților  
- identificarea și documentarea bug-urilor  

---

### 🎨 Frontend & UX Developer
- dezvoltarea interfeței web  
- implementarea vizualizării în timp real a procesului agenților  
- afișarea rezultatelor intermediare și finale  
- funcționalități de export și interacțiune cu utilizatorul  
