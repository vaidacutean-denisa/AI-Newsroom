# 🧪 Metodologia de Evaluare: LLM-as-a-Judge (G-Eval)

Acest document descrie fundamentul academic și detaliile de implementare pentru sistemul de evaluare automată a calității articolelor din cadrul proiectului **AI-Newsroom**.

---

## 📖 1. Fundamente Teoretice

În mod tradițional, evaluarea textelor generate prin sisteme de Natural Language Generation (NLG) se baza pe metrici lexicale precum:
* **BLEU (Bilingual Evaluation Understudy)**: Măsoară precizia n-gramelor între textul generat și referințe. Folosit în principal în traduceri.
* **ROUGE (Recall-Oriented Understudy for Gisting Evaluation)**: Măsoară gradul de acoperire al n-gramelor (recall). Folosit în principal în rezumate.

### ⚠️ Limitarea Metricilor Clasice
Metricile bazate exclusiv pe suprapunerea lexicală (BLEU, ROUGE) suferă de o mare problemă: **nu înțeleg semantica**. Dacă un model generează o propoziție corectă și coerentă folosind sinonime sau reformulări care nu apar în textul de referință, metricile clasice o vor penaliza cu un scor foarte mic, deși calitatea umană percepută este maximă.

### 🌟 Soluția Modernă: G-Eval (LLM-as-a-Judge)
Inspirat din lucrarea academică **"G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment"** *(Liu et al., 2023, arXiv:2303.16634)*, proiectul utilizează un model de limbaj (LLM) ca judecător automat. 

Cercetările arată că LLM-urile puternice, atunci când sunt ghidate de instrucțiuni de evaluare (prompts) precise și formulează o justificare rațională înainte de a acorda o notă, prezintă o **corelație mult mai mare cu evaluarea umană** comparativ cu BLEU sau ROUGE.

---

## 📐 2. Criterii de Evaluare Implementate

Evaluatorul nostru analizează articolul generat pe baza a două dimensiuni calitative adaptate din standardele de evaluare academică:

### A. Coerență (Coherence)
* **Definiție**: Măsura în care textul final este bine structurat, ușor de citit, organizat logic și lipsit de contradicții interne sau fraze repetitive.
* **Scară de notare**: 1-5 (1 = text indescifrabil/haotic; 5 = articol cursiv, perfect organizat în Markdown).

### B. Relevanță (Relevance)
* **Definiție**: Măsura în care articolul final acoperă fidel subiectul și ideile cheie prezente în draftul inițial propus de Jurnalist, fără a introduce detalii inutile sau complet divergente.
* **Scară de notare**: 1-5 (1 = complet irelevant; 5 = acoperire totală și fidelă).

---

## 🛠️ 3. Implementarea Tehnică

Procesul este implementat în scriptul [scripts/ai_evals.py](file:///c:/Users/noemi/Desktop/MDS/AI-Newsroom/scripts/ai_evals.py):

```mermaid
graph TD
    A[Utilizator introduce subiectul] --> B[Agent Jurnalist: Draft brut]
    B --> C[Agent Editor: Feedback & Articol final]
    C --> D[Evaluator: LLM-as-a-Judge]
    D --> E{Scoruri >= 3/5?}
    E -- Da --> F[Validat cu succes]
    E -- Nu --> G[Eșec evaluare & Sys Exit 1]
```

1. **Promptul Evaluatorului**: Ghidează LLM-ul să joace rolul unui arbitru obiectiv și îl forțează să returneze un format strict JSON conținând `coherence_score`, `relevance_score` și `reasoning`.
2. **Modul CI (Continuous Integration)**: Pentru a fi integrat în GitHub Actions fără a depinde de o instanță activă de Ollama în cloud, scriptul detectează mediul (`CI=true`) și simulează un răspuns valid al judecătorului.
3. **Local**: Apelează API-ul `/ask` al aplicației FastAPI, delegând evaluarea către modelul `mistral` din Ollama.
