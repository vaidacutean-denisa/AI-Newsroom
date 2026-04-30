# 📐 System Architecture

## 🧱 UML Component Diagram

```plantuml
@startuml
actor Utilizator

package "Frontend Layer" {
  [Frontend] as FE
}

package "Backend Layer" {
  [Backend (Orchestrator)] as BE
}

package "Agent Layer" {
  [Agent 1 (Cercetare)] as A1
  [Agent 2 (Sinteză)] as A2
}

database "Local LLM (Ollama)" as LLM

Utilizator --> FE
FE --> BE
BE --> A1
BE --> A2
A1 --> LLM
A2 --> LLM

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

