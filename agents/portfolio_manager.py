# agents/portfolio_manager.py

from shared.api_client import api

MIN_MVP_COST = 10000  # Example cost in USD
MIN_DEV_UNITS = 2     # Example unit of developer agent capacity

class PortfolioManagerAgent:
    """Implementation of the PortfolioManagerAgent's logic."""

    def evaluate_new_ideas(self):
        print("\n--- Evaluating New Ideas ---")
        top_ideas = api.get("/idea_validator/top_ideas", params={"status": "validated", "limit": 5})
        # financial_status = api.get("/financial_allocator/status") # Not mocked yet
        # dev_status = api.get("/orchestrator/dev_capacity") # Not mocked yet

        # Mocking resource availability
        financial_status = {'discretionary_capital': 20000}
        dev_status = {'available_units': 5}

        if financial_status['discretionary_capital'] < MIN_MVP_COST or dev_status['available_units'] < MIN_DEV_UNITS:
            print("HOLD: Insufficient capital or development resources.")
            return

        if not top_ideas:
            print("HOLD: No suitable candidates.")
            return

        # Simplified scoring for scaffold
        best_candidate = top_ideas[0]
        print(f"GO: Greenlighting new SaaS: {best_candidate['name']}")
        api.post("/orchestrator/dispatch_job", json={
            "job_type": "INCUBATE_MVP",
            "idea_id": best_candidate['id']
        })
        api.post("/financial_allocator/allocate", json={
            "idea_id": best_candidate['id'],
            "amount": MIN_MVP_COST,
            "purpose": "Initial MVP incubation"
        })

    def review_portfolio_performance(self):
        print("\n--- Reviewing Portfolio Performance (Quarterly) ---")
        live_products = [{"id": "saas_001", "name": "AI-Writer", "consecutive_bad_quarters": 0}] # Mock

        for saas in live_products:
            metrics = api.get(f"/saas_portfolio/{saas['id']}/metrics", params={"period": "90d"})
            health_score = (
                metrics['mrr_growth'] * 0.4 +
                metrics['user_satisfaction'] * 0.3 +
                (1 - metrics['churn_rate']) * 0.2 +
                metrics['profit_margin'] * 0.1
            )

            decision = "MAINTAIN"
            if health_score > 0.8 and metrics['mrr_growth'] > 0.1:
                decision = "GROW"
                print(f"DECISION for {saas['name']}: GROW (Health: {health_score:.2f})")
                api.post("/campaign_manager/update_budget", json={"saas_id": saas['id'], "increase_percentage": 0.20})
            elif health_score < 0.4 and saas['consecutive_bad_quarters'] >= 1:
                decision = "SUNSET"
                print(f"DECISION for {saas['name']}: SUNSET (Health: {health_score:.2f})")
                api.post("/saas_flip_engine/attempt_sale", json={"saas_id": saas['id']})
            else:
                print(f"DECISION for {saas['name']}: MAINTAIN (Health: {health_score:.2f})")

            api.patch(f"/saas_portfolio/{saas['id']}", json={"status": decision, "health_score": health_score})
