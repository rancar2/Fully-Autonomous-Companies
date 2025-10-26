## 3. System Architecture Diagram (Fortified)

This document provides a description and diagram of the full AI-first architecture for the meta-SaaS platform, updated to reflect the Fortified Strategy.

---

```mermaid
graph TD
    subgraph "Human Oversight"
        A[Human Board of Directors]
    end

    subgraph "Interface Layer"
        B[Web UI / Admin Dashboard]
        C[API / Webhooks]
    end

    subgraph "Governance Layer"
        D[CEO Agent]
        E[CFO Agent]
        F[CTO Agent]
    end

    subgraph "Orchestration & Agent Layer"
        G[LangGraph / CrewAI]
        H[Specialized Agents]
    end

    subgraph "Execution & Development Layer"
        I[Rails 8 + SolidQueue]
        J[Kamal 2 Deployer]
    end

    subgraph "Shared Memory & Data Layer"
        K[Vector DB (Chroma/Weaviate)]
        L[SQLite Application DB]
        M[Immutable Audit Logs]
    end

    A -- Interacts via --> B;
    B --> D;
    C --> D;

    D -- Directs --> G;
    E -- Directs --> G;
    F -- Directs --> G;

    G -- Executes --> H;
    H -- Use --> I;
    H -- Use --> J;

    H -- Access --> K;
    I -- Access --> L;
    H -- Write to --> M;
```

### Core Layers

1.  **Human Oversight**
    *   The **Human Board of Directors** provides high-level governance, sets budgets, and has ultimate control over the system.

2.  **Interface Layer**
    *   **Web UI:** An administration dashboard for the Board of Directors to monitor the system and make high-level decisions.
    *   **API:** An API for programmatic interaction and integration with external systems.

3.  **Governance Layer**
    *   The **Trinity of Agents (CEO, CFO, CTO)** forms the core decision-making unit of the autonomous business. They direct the overall strategy, manage finances, and oversee the technical implementation.

4.  **Orchestration & Agent Layer**
    *   **Orchestrator (LangGraph/CrewAI):** Manages the execution of tasks and the coordination of the specialized agents.
    *   **Specialized Agents:** A team of agents responsible for specific operational tasks (e.g., `Coder`, `Marketer`, `Guardian`).

5.  **Execution & Development Layer**
    *   **Tech Stack:** Ruby on Rails 8, SolidQueue, and Bun provide the core application framework and job queuing system.
    *   **Deployment:** Kamal 2 is used for automated deployment to cloud infrastructure.

6.  **Shared Memory & Data Layer**
    *   **Vector DB:** A vector database like ChromaDB or Weaviate for agent memory.
    *   **Application DB:** An SQLite database for the application's operational data.
    *   **Immutable Audit Logs:** A secure, tamper-proof log of all agent actions and decisions, managed by the `Auditor Agent`.
