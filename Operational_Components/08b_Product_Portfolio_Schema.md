# Product Portfolio Database Schema

## 1. Objective

To define the canonical database schema for `SaaS_Portfolio.db`. This database is the single source of truth for the entire product lifecycle, from initial idea to final sunset. It is designed to be used with SQLite to maintain simplicity and portability.

## 2. Schema Definition (SQL)

Below are the `CREATE TABLE` statements for each table in the database.

### `ideas`

Stores all product ideas, both raw and validated. This table is the input for the `PortfolioManagerAgent`'s greenlight process.

```sql
CREATE TABLE ideas (
    idea_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    source_url TEXT, -- Where the idea came from (e.g., Reddit URL)
    status TEXT NOT NULL CHECK(status IN ('new', 'validating', 'validated', 'rejected', 'incubating')) DEFAULT 'new',
    viability_score REAL, -- A score from 0.0 to 1.0, null until validated
    business_case_json TEXT, -- A JSON blob containing TAM, competition, etc.
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### `saas_products`

Stores the core information for each SaaS product that has been greenlit for incubation.

```sql
CREATE TABLE saas_products (
    saas_id INTEGER PRIMARY KEY AUTOINCREMENT,
    idea_id INTEGER NOT NULL,
    name TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL CHECK(status IN ('incubating', 'live', 'maintain', 'grow', 'sunsetting', 'sunset')) DEFAULT 'incubating',
    health_score REAL, -- The latest calculated health score
    consecutive_bad_quarters INTEGER DEFAULT 0, -- Incremented if health_score is low
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    live_at DATETIME, -- Timestamp when it first went live
    sunset_at DATETIME, -- Timestamp when it was officially shut down
    FOREIGN KEY (idea_id) REFERENCES ideas (idea_id)
);
```

### `performance_metrics`

A time-series table to log the performance of each live SaaS product over time. This is the primary data source for the `PortfolioManagerAgent`'s review process.

```sql
CREATE TABLE performance_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    saas_id INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    mrr REAL NOT NULL, -- Monthly Recurring Revenue
    mrr_growth REAL NOT NULL, -- Month-over-month growth rate
    churn_rate REAL NOT NULL, -- Customer churn rate
    active_users INTEGER NOT NULL,
    user_satisfaction_score REAL, -- e.g., from 0.0 to 1.0
    profit_margin REAL NOT NULL, -- (Revenue - Costs) / Revenue
    FOREIGN KEY (saas_id) REFERENCES saas_products (saas_id)
);

-- Create an index for faster time-series queries
CREATE INDEX idx_performance_metrics_saas_time ON performance_metrics (saas_id, timestamp DESC);
```

### `resource_allocations`

Logs all resource allocation decisions made by the strategic agents.

```sql
CREATE TABLE resource_allocations (
    allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    saas_id INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    dev_agent_units INTEGER, -- Number of developer agent cycles allocated
    marketing_budget_usd REAL, -- Marketing budget allocated in USD
    purpose TEXT, -- e.g., "Quarterly GROW decision"
    FOREIGN KEY (saas_id) REFERENCES saas_products (saas_id)
);
```
