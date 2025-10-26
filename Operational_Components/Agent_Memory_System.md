## 5. Agent Memory & Self-Reflection System

To ensure the meta-SaaS platform is robust, adaptive, and continuously improving, the agents are equipped with a system for persistent memory, self-evaluation, and long-term reflection.

---

### ⚙️ Architecture Overview

```
+------------------------+
|   Agent Memory Store   |
+------------------------+
| - Task Logs            |
| - Agent Reflections    |
| - User Feedback        |
| - System Snapshots     |
+------------------------+
          |
          v
+--------------------------+
| Agent Self-Evaluator     |
+--------------------------+
| - Prompt Tuner           |
| - Reward Function Learner|
| - Anomaly Detector       |
+--------------------------+
          |
          v
+---------------------------+
| Memory Summarizer Agent   |
+---------------------------+
| - Weekly Digest Generator |
| - Embedding Compressor    |
+---------------------------+
```

### 🧩 Key Components

#### 🗃️ 1. Long-Term Memory Store

Every task performed by an agent is recorded in a database (e.g., SQLite with `pgvector`-like embedding indexing) with the following fields:

| Field           | Description                                      |
|-----------------|--------------------------------------------------|
| `agent_id`      | Unique agent name (e.g., `scaffolder-1`)         |
| `timestamp`     | UTC time of the action                           |
| `task_summary`  | One-line human-readable summary of the task      |
| `input_context` | The prompt and environment snapshot for the task |
| `output_result` | The final output blob from the agent             |
| `score`         | A self-evaluated score (0–1) for the task        |
| `feedback_id`   | A link to any user or human input                |
| `error_flag`    | Null or an error type (e.g., `code_invalid`)     |

**Storage Tech Stack:** LiteFS + SQLite + Bun-based REST server for querying.

#### 🔁 2. Reflection Triggers

Agents trigger a self-evaluation process under the following conditions:

*   A task **fails** after a retry or failover.
*   A human (founder) provides **negative feedback** (e.g., a "thumbs down").
*   A **pattern of errors** is detected (e.g., >3 similar failures).
*   On a **weekly cadence** for summarization.

Each reflection is stored as a JSON object with the following fields:

| Field              | Purpose                                     |
|--------------------|---------------------------------------------|
| `what_went_well`   | Extracts positive patterns from the task.   |
| `what_went_wrong`  | Detects errors and their root causes.       |
| `next_time_try`    | Proposes a modification to the prompt or approach. |
| `confidence_shift` | A float delta (+/−) based on the learning.  |

#### 🧠 3. Summarizer Agent

Every 7 days, a Summarizer Agent performs the following tasks:

*   Pulls the top 50 task logs for each agent.
*   Summarizes the key learnings in a markdown format.
*   Updates the **agent-specific README** in a GitOps pattern.
*   Compresses the embedding memory window into the vector store, retaining the top 10 clusters.

This process keeps the agents lean while allowing them to continuously improve their performance.

#### 🔐 4. Memory Privacy & Data Contracts

To ensure data privacy, every data object has:

*   A `retention_policy` (e.g., 7 days, 30 days, or never).
*   A `sensitivity_flag` (e.g., to indicate if it contains user PII).
*   An option for users to fully **opt out** via their settings.

Memory is treated as **data exhaust**, not personal data, unless explicitly marked otherwise.
