# 📐 System Architecture

## 🧱 UML Component Diagram

```plantuml
@startuml
actor Utilizator

package "Frontend Layer" {
  [Frontend]
}

package "Backend Layer" {
  [Backend (Orchestrator)]
}

package "Agent Layer" {
  [Agent 1 (Cercetare)]
  [Agent 2 (Sinteză)]
}

database "Local LLM (Ollama)" as LLM

Utilizator --> Frontend
Frontend --> Backend (Orchestrator)
Backend (Orchestrator) --> Agent 1 (Cercetare)
Backend (Orchestrator) --> Agent 2 (Sinteză)
Agent 1 (Cercetare) --> LLM
Agent 2 (Sinteză) --> LLM
@enduml
```

---

## 🔄 Agent Workflow Diagram

```mermaid
sequenceDiagram
    autonumber
    participant U as Utilizator
    participant F as Frontend
    participant B as Backend (Orchestrator)
    participant A1 as Agent 1 (Cercetare)
    participant A2 as Agent 2 (Sinteză)

    U->>F: Introduce cererea
    F->>B: Trimite request către API
    B->>A1: Solicită colectare date
    A1-->>B: Returnează informații brute
    B->>A2: Solicită sinteză
    A2-->>B: Returnează raport final
    B-->>F: Trimite răspunsul final
    F-->>U: Afișează rezultatul
```

---

## 📝 Notes

> Diagrams generated with AI assistance (ChatGPT + Mermaid / PlantUML).  
> PlantUML diagram may require a compatible viewer (e.g. VS Code extension or PlantUML renderer).

