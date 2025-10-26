# CapitalAllocatorAgent Logic Specification

## 1. Objective

To define the core logic for the `CapitalAllocatorAgent`, the AI-CFO responsible for making strategic, high-level financial decisions. Its primary role is to apply a configurable policy to the company's net profits, deciding how to allocate capital to maximize the portfolio's long-term value.

## 2. Primary Function: `allocate_monthly_profits()`

This function is the agent's entire purpose. It is triggered on a monthly cycle after the `FinancialAnalystAgent` has finalized the previous month's P&L.

**Pseudocode:**

```python
def allocate_monthly_profits():
    # 1. Get Financial Summary and Allocation Policy
    financial_summary = api.get("/financial_analyst/monthly_summary")
    net_profit = financial_summary['net_profit_usd']

    # The policy is a simple JSON file, allowing for high-level human guidance
    allocation_policy = load_json_from_file("CapitalAllocationPolicy.json")

    print(f"Monthly cycle starting. Net Profit: ${net_profit}. Applying policy: {allocation_policy['policy_name']}.")

    if net_profit <= 0:
        print("No profit to allocate. Cycle ends.")
        return

    # 2. Apply Allocation Policy
    allocations = allocation_policy['allocations']

    # 2a. Allocate to Reinvestment/Growth
    if allocations['reinvest_growth'] > 0:
        amount = net_profit * allocations['reinvest_growth']
        # Get top-performing SaaS products from the Portfolio Manager
        growth_candidates = api.get("/portfolio_manager/recommendations?type=grow&limit=3")
        if growth_candidates:
            # Distribute the amount among the top candidates
            for candidate in growth_candidates:
                allocation_amount = amount / len(growth_candidates)
                print(f"Allocating ${allocation_amount} to GROW {candidate['name']}.")
                api.post("/campaign_manager/update_budget", json={
                    "saas_id": candidate['saas_id'],
                    "increase_amount": allocation_amount
                })

    # 2b. Allocate to New Ventures
    if allocations['fund_new_ventures'] > 0:
        amount = net_profit * allocations['fund_new_ventures']
        print(f"Allocating ${amount} to the NEW VENTURE incubation fund.")
        # This amount is added to the discretionary capital pool for the PortfolioManagerAgent
        api.post("/financial_allocator/add_to_discretionary_capital", json={"amount": amount})

    # 2c. Allocate to Cash Reserves
    if allocations['cash_reserves'] > 0:
        amount = net_profit * allocations['cash_reserves']
        print(f"Allocating ${amount} to cash reserves.")
        api.post("/financial_allocator/add_to_reserves", json={"amount": amount})

    # 2d. Allocate to Profit Distribution (for DAOs or external owners)
    if allocations['profit_distribution'] > 0:
        amount = net_profit * allocations['profit_distribution']
        print(f"Allocating ${amount} for profit distribution.")
        api.post("/external_payments/distribute_profit", json={"amount": amount})

    print("Capital allocation cycle complete.")
```

## 3. The Capital Allocation Policy File

The `CapitalAllocationPolicy.json` file is the key mechanism for high-level strategic control. It is human-readable and can be updated to change the company's financial behavior without altering agent code.

**Example `CapitalAllocationPolicy.json`:**

```json
{
  "policy_name": "Balanced Growth",
  "description": "A balanced approach focusing on growing existing winners while still funding new ideas and building a cash buffer.",
  "allocations": {
    "reinvest_growth": 0.50,      // 50% of profits go to marketing/dev for successful products
    "fund_new_ventures": 0.25,  // 25% of profits go to the fund for building new MVPs
    "cash_reserves": 0.20,      // 20% of profits are saved as a cash buffer
    "profit_distribution": 0.05 // 5% is distributed to owners/DAO
  }
}
```

## 4. API Interactions (Contracts)

- **`GET /financial_analyst/monthly_summary`**: Returns `{net_profit_usd: float}`.
- **`GET /portfolio_manager/recommendations`**: Returns a ranked list of SaaS products suitable for a specific action (e.g., `type=grow`).
- **`POST /campaign_manager/update_budget`**: Increases the marketing budget for a specific SaaS.
- **`POST /financial_allocator/add_to_discretionary_capital`**: Adds funds to the pool used by `PortfolioManagerAgent` to fund new MVPs.
- **`POST /financial_allocator/add_to_reserves`**: Moves capital into a secure, non-operational reserve fund.
- **`POST /external_payments/distribute_profit`**: Initiates a payment to an external entity (e.g., a DAO treasury wallet).
