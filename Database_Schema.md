## Database Schema

This document defines the database schema for the core models of the autonomous meta-SaaS platform. The schema is designed to support the operations of the various agents and the overall business logic.

---

### `users` table

Stores information about the users of the meta-SaaS platform (the "investors" or "Board of Directors").

| Column Name      | Data Type | Description                                      |
|------------------|-----------|--------------------------------------------------|
| `id`             | `INTEGER` | Primary Key                                      |
| `email`          | `TEXT`    | The user's email address.                        |
| `hashed_password`| `TEXT`    | The user's hashed password.                      |
| `created_at`     | `DATETIME`| The timestamp when the user was created.         |
| `updated_at`     | `DATETIME`| The timestamp when the user was last updated.    |

### `saas_products` table

Stores information about the SaaS products that are generated and managed by the platform.

| Column Name      | Data Type | Description                                      |
|------------------|-----------|--------------------------------------------------|
| `id`             | `INTEGER` | Primary Key                                      |
| `name`           | `TEXT`    | The name of the SaaS product.                    |
| `description`    | `TEXT`    | A brief description of the SaaS product.         |
| `status`         | `TEXT`    | The current status of the product (e.g., `idea`, `validating`, `building`, `live`, `sunsetting`). |
| `user_id`        | `INTEGER` | Foreign key to the `users` table (the owner).    |
| `created_at`     | `DATETIME`| The timestamp when the product was created.      |
| `updated_at`     | `DATETIME`| The timestamp when the product was last updated.   |

### `agent_tasks` table

Stores a log of all tasks performed by the agents.

| Column Name      | Data Type | Description                                      |
|------------------|-----------|--------------------------------------------------|
| `id`             | `INTEGER` | Primary Key                                      |
| `agent_name`     | `TEXT`    | The name of the agent that performed the task.   |
| `task_name`      | `TEXT`    | The name of the task that was performed.         |
| `input`          | `TEXT`    | The input parameters for the task.               |
| `output`         | `TEXT`    | The output of the task.                          |
| `status`         | `TEXT`    | The status of the task (e.g., `success`, `failure`). |
| `error_message`  | `TEXT`    | Any error message if the task failed.            |
| `created_at`     | `DATETIME`| The timestamp when the task was created.         |

### `financials` table

Stores financial data for the meta-SaaS platform and each spawned SaaS product.

| Column Name      | Data Type | Description                                      |
|------------------|-----------|--------------------------------------------------|
| `id`             | `INTEGER` | Primary Key                                      |
| `saas_product_id`| `INTEGER` | Foreign key to the `saas_products` table (nullable, for platform-level financials). |
| `metric_name`    | `TEXT`    | The name of the financial metric (e.g., `MRR`, `CAC`, `LTV`, `api_cost`). |
| `value`          | `REAL`    | The value of the metric.                         |
| `recorded_at`    | `DATETIME`| The timestamp when the metric was recorded.      |

### `audit_log` table

Stores an immutable log of all agent actions for compliance and security purposes.

| Column Name      | Data Type | Description                                      |
|------------------|-----------|--------------------------------------------------|
| `id`             | `INTEGER` | Primary Key                                      |
| `agent_name`     | `TEXT`    | The name of the agent that performed the action. |
| `action`         | `TEXT`    | A description of the action that was performed.  |
| `details`        | `TEXT`    | Any additional details about the action.         |
| `signature`      | `TEXT`    | A cryptographic signature to ensure immutability.|
| `created_at`     | `DATETIME`| The timestamp when the action was logged.        |
