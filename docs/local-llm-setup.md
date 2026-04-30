# Documentație Tehnică: Implementare LLM Local (Ollama)

Acest document descrie configurarea, instalarea și integrarea modelelor de limbaj rulate local, eliminând dependența de API-uri externe pentru a asigura confidențialitatea datelor și stabilitatea sistemului.

---

## 1. Precondiții Software
Pentru execuția modelelor, utilizăm **Ollama**, un motor performant care permite rularea modelelor cuantizate cu consum optimizat de resurse.

*   **Sistem de operare:** Windows 10+, macOS, sau Linux.
*   **Hardware minim:** 8GB RAM (16GB recomandat) și suport GPU (opțional).

---

## 2. Ghid de Instalare și Setup

### Pasul 1: Instalarea motorului Ollama
*   **Windows/macOS:** Descărcați kit-ul de instalare de pe [ollama.com](https://ollama.com).
*   **Linux:** Executați următoarea comandă în terminal:
    ```bash
    curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
    ```

### Pasul 2: Descărcarea modelului (ex: Mistral)
Odată instalat Ollama, descărcați modelul stabilit pentru proiect folosind CLI:
```bash
ollama pull mistral
```

### Pasul 3: Verificarea serviciului
Serviciul rulează implicit pe portul `11434`. Puteți verifica dacă este activ accesând `http://localhost:11434` în browser.

---

## 3. Integrarea cu Backend-ul
Backend-ul comunică cu modelul local prin cereri HTTP POST către endpoint-ul nativ al Ollama.

**Endpoint:** `http://localhost:11434/api/generate`

**Structură cerere (JSON):**
```json
{
  "model": "mistral",
  "prompt": "Introduceți textul aici...",
  "stream": false
}
```

---

## 4. Gestionarea Erorilor (Resilience)
Conform criteriilor de acceptare, sistemul gestionează următoarele scenarii:

*   **Serviciul Offline:** Dacă motorul Ollama nu rulează, backend-ul returnează un cod `HTTP 503 Service Unavailable`.
*   **Timeout:** Cererile au un prag de timeout setat pentru a preveni blocarea aplicației.
*   **Erori HTTP:** Orice eroare de la motorul LLM este logată și trimisă sub formă de excepție controlată.

---

## 5. Comenzi Utile pentru Devs
*   `ollama list` - Afișează toate modelele instalate local.
*   `ollama run mistral` - Testează modelul direct în terminal.
*   `ollama rm [nume_model]` - Șterge un model pentru a elibera spațiu.

---
