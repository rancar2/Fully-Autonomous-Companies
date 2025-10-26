# Financial Ledger Database Schema

## 1. Objective

To define the schema for the `MasterLedger.db`, the immutable, auditable single source of truth for all financial transactions across the entire autonomous operation. Its design prioritizes traceability and simplicity, behaving like a traditional accounting ledger.

## 2. Design Principles

- **Immutability:** Transactions are never updated or deleted. Corrections are made via new, reversing transactions.
- **Double-Entry:** Every transaction involves a debit from one account and a credit to another, ensuring the books are always balanced.
- **Traceability:** Every transaction is linked to a source agent or event.

## 3. Schema Definition (SQL)

### `accounts`

Defines the chart of accounts. This is a static table that lists all the financial accounts in the system.

```sql
CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE, -- e.g., "Stripe Revenue", "AWS Costs", "Cash Reserves"
    type TEXT NOT NULL CHECK(type IN ('asset', 'liability', 'equity', 'revenue', 'expense')),
    balance REAL NOT NULL DEFAULT 0.0
);
```

-- Populate with initial accounts
-- INSERT INTO accounts (name, type) VALUES ('Cash', 'asset');
-- INSERT INTO accounts (name, type) VALUES ('Stripe Revenue', 'revenue');
-- INSERT INTO accounts (name, type) VALUES ('AWS Hosting Costs', 'expense');
-- INSERT INTO accounts (name, type) VALUES ('OpenAI API Costs', 'expense');
-- INSERT INTO accounts (name, type) VALUES ('Marketing Ad Spend', 'expense');
-- INSERT INTO accounts (name, type) VALUES ('Discretionary Capital Fund', 'asset');
-- INSERT INTO accounts (name, type) VALUES ('Cash Reserves', 'asset');
-- INSERT INTO accounts (name, type) VALUES ('Owners Equity', 'equity');

### `transactions`

The core immutable log of all financial events. A single "event" (like a Stripe payment) will result in two entries here (a debit and a credit).

```sql
CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL, -- A unique ID grouping all entries for a single event
    account_id INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    type TEXT NOT NULL CHECK(type IN ('debit', 'credit')),
    amount REAL NOT NULL CHECK(amount > 0),
    description TEXT NOT NULL, -- e.g., "Monthly subscription payment for SaaS-A from customer #123"
    source_agent TEXT, -- The agent that initiated the transaction, e.g., 'FinancialAnalystAgent'
    source_reference_id TEXT, -- e.g., a Stripe charge ID or an AWS bill ID
    FOREIGN KEY (account_id) REFERENCES accounts (account_id)
);

-- Create indexes for faster queries
CREATE INDEX idx_transactions_event_id ON transactions (event_id);
CREATE INDEX idx_transactions_account_id ON transactions (account_id);
```

## 4. Example Transaction Flow

**Event:** A customer pays a $20 subscription fee for "SaaS-A" via Stripe.

**Process:** The `FinancialAnalystAgent` detects the Stripe payment.

1.  It generates a unique `event_id`, e.g., `evt_stripe_123abc`.
2.  It creates two entries in the `transactions` table:

    -   **Entry 1 (Credit):**
        -   `event_id`: `evt_stripe_123abc`
        -   `account_id`: (ID for 'Stripe Revenue')
        -   `type`: `credit`
        -   `amount`: `20.00`
        -   `description`: `Subscription revenue for SaaS-A`

    -   **Entry 2 (Debit):**
        -   `event_id`: `evt_stripe_123abc`
        -   `account_id`: (ID for 'Cash')
        -   `type`: `debit`
        -   `amount`: `20.00`
        -   `description`: `Cash received from Stripe payment`

3.  It updates the `balance` in the `accounts` table for both 'Stripe Revenue' and 'Cash'.

This ensures that for every event, `SUM(debits) == SUM(credits)`, and the integrity of the financial system is maintained at all times.
