# Meta-Learning Database Schema

## 1. Objective

To define the schema for the `Meta_Learning.db`, the database that stores all information required for the `MetaMindAgent` to learn and make decisions. It acts as the memory for the entire system's self-improvement journey.

## 2. Schema Definition (SQL)

### `agent_performance_logs`

A time-series table that logs the performance of every individual agent job execution.

```sql
CREATE TABLE agent_performance_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT NOT NULL, -- e.g., 'ContentCreatorAgent', 'PortfolioManagerAgent'
    job_id TEXT NOT NULL UNIQUE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    execution_time_ms INTEGER NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('success', 'failure')),
    error_message TEXT, -- Null if successful
    resource_consumption_json TEXT, -- JSON blob with CPU, memory, API calls used
    llm_confidence_score REAL -- The confidence score of the LLM for its output, if applicable
);

CREATE INDEX idx_agent_performance_agent_time ON agent_performance_logs (agent_name, timestamp DESC);
```

### `system_kpis`

A time-series table that logs the highest-level business and operational Key Performance Indicators (KPIs).

```sql
CREATE TABLE system_kpis (
    kpi_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_mrr REAL NOT NULL,
    net_profit_usd REAL NOT NULL,
    active_saas_products INTEGER NOT NULL,
    system_wide_error_rate REAL NOT NULL, -- Percentage of all agent jobs that failed
    customer_churn_rate_avg REAL NOT NULL -- Average churn across all SaaS products
);
```

### `meta_experiments`

Stores the record of every self-improvement experiment conceived and run by the `MetaMindAgent`.

```sql
CREATE TABLE meta_experiments (
    experiment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    hypothesis TEXT NOT NULL, -- The full 'IF X, THEN Y, BECAUSE Z' statement
    status TEXT NOT NULL CHECK(status IN ('pending', 'running', 'success', 'failure', 'rejected')),
    target_metric TEXT NOT NULL, -- The specific metric this experiment was intended to improve
    ab_test_id TEXT, -- The ID of the A/B test run by the orchestrator
    start_time DATETIME,
    end_time DATETIME,
    results_summary_json TEXT -- JSON blob summarizing the outcome
);
```
