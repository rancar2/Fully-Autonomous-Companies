# agents/capital_allocator.py

import json
from shared.api_client import api

class CapitalAllocatorAgent:
    """Implementation of the CapitalAllocatorAgent's logic."""

    def allocate_monthly_profits(self):
        print("\n--- Allocating Monthly Profits ---")
        financial_summary = api.get("/financial_analyst/monthly_summary")
        net_profit = financial_summary['net_profit_usd']

        # Load policy from file - in a real system, this file would be managed carefully
        try:
            with open("CapitalAllocationPolicy.json", "r") as f:
                allocation_policy = json.load(f)
        except FileNotFoundError:
            print("CRITICAL: CapitalAllocationPolicy.json not found. Using default.")
            allocation_policy = {
                "policy_name": "Default Balanced",
                "allocations": {"reinvest_growth": 0.5, "fund_new_ventures": 0.3, "cash_reserves": 0.2}
            }

        print(f"Net Profit: ${net_profit}. Applying policy: {allocation_policy['policy_name']}.")

        if net_profit <= 0:
            print("No profit to allocate.")
            return

        allocations = allocation_policy['allocations']

        if allocations.get('reinvest_growth', 0) > 0:
            amount = net_profit * allocations['reinvest_growth']
            print(f"Allocating ${amount} to GROW existing products.")
            # In a real system, this would be distributed to top SaaS products
            api.post("/campaign_manager/update_budget", json={"increase_amount": amount, "saas_id": "saas_001"})

        if allocations.get('fund_new_ventures', 0) > 0:
            amount = net_profit * allocations['fund_new_ventures']
            print(f"Allocating ${amount} to the NEW VENTURE incubation fund.")
            api.post("/financial_allocator/add_to_discretionary_capital", json={"amount": amount})

        if allocations.get('cash_reserves', 0) > 0:
            amount = net_profit * allocations['cash_reserves']
            print(f"Allocating ${amount} to cash reserves.")
            api.post("/financial_allocator/add_to_reserves", json={"amount": amount})

        print("Capital allocation cycle complete.")
