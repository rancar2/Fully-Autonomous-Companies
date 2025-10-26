# PortfolioManagerAgent Logic Specification

## 1. Objective

To define the core, implementable decision-making logic for the `PortfolioManagerAgent`. This agent acts as the executive decision-maker for the entire SaaS portfolio, determining which products get built, funded, and retired.

## 2. Primary Functions & Logic

### 2.1. `evaluate_new_ideas()`

This function is triggered on a weekly cycle or when a high-potential idea is discovered.

**Pseudocode:**

```python
def evaluate_new_ideas():
    # 1. Fetch top-ranked, validated ideas
    # Ideas are pre-scored by the IdeaValidatorAgent
    top_ideas = api.get("/idea_validator/top_ideas?status=validated&limit=5")

    # 2. Check for available resources
    financial_status = api.get("/financial_allocator/status")
    dev_status = api.get("/orchestrator/dev_capacity")

    if financial_status['discretionary_capital'] < MIN_MVP_COST or dev_status['available_units'] < MIN_DEV_UNITS:
        print("HOLD: Insufficient capital or development resources.")
        return {"decision": "HOLD", "reason": "Insufficient resources"}

    # 3. Calculate a final priority score for each idea
    scored_candidates = []
    for idea in top_ideas:
        # Diversification score is lower if we already have a similar product
        diversification_score = calculate_diversification(idea, portfolio.get_all_saas())
        # Strategic fit score is higher if the idea aligns with long-term goals
        strategic_fit_score = calculate_strategic_fit(idea)

        # Final score weights viability most heavily
        priority_score = (idea['viability_score'] * 0.6) + (diversification_score * 0.2) + (strategic_fit_score * 0.2)
        scored_candidates.append({"idea": idea, "priority_score": priority_score})

    # 4. Select the best candidate
    if not scored_candidates:
        return {"decision": "HOLD", "reason": "No suitable candidates"}

    best_candidate = max(scored_candidates, key=lambda x: x['priority_score'])

    # 5. Issue GO command and allocate resources
    print(f"GO: Greenlighting new SaaS: {best_candidate['idea']['name']}")
    api.post("/orchestrator/dispatch_job", json={
        "job_type": "INCUBATE_MVP",
        "idea_id": best_candidate['idea']['id']
    })
    api.post("/financial_allocator/allocate", json={
        "saas_id": None, # Will be created by the new job
        "amount": MIN_MVP_COST,
        "purpose": "Initial MVP incubation"
    })

    return {"decision": "GO", "idea_id": best_candidate['idea']['id']}

```

### 2.2. `review_portfolio_performance()`

This function is triggered on a quarterly cycle for every `live` or `maintain` SaaS product.

**Pseudocode:**

```python
def review_portfolio_performance():
    live_products = api.get("/saas_portfolio/all?status=live,maintain")

    for saas in live_products:
        # 1. Get performance metrics for the last 90 days
        metrics = api.get(f"/saas_portfolio/{saas['id']}/metrics?period=90d")

        # 2. Calculate a composite health score
        # Weights can be tuned by the meta-learning engine
        health_score = (
            metrics['mrr_growth'] * 0.4 +
            metrics['user_satisfaction'] * 0.3 +
            (1 - metrics['churn_rate']) * 0.2 +
            metrics['profit_margin'] * 0.1
        )

        # 3. Apply the decision tree
        decision = "MAINTAIN" # Default decision

        if health_score > 0.8 and metrics['mrr_growth'] > 0.1:
            decision = "GROW"
            print(f"DECISION for {saas['name']}: GROW")
            # Allocate more budget for marketing
            api.post("/campaign_manager/update_budget", json={
                "saas_id": saas['id'],
                "increase_percentage": 0.20
            })
            # Activate RoadmapAgent to build new features
            api.post("/orchestrator/dispatch_job", json={
                "job_type": "GENERATE_ROADMAP",
                "saas_id": saas['id']
            })

        elif health_score < 0.4 and saas['consecutive_bad_quarters'] >= 1:
            decision = "SUNSET"
            print(f"DECISION for {saas['name']}: SUNSET")
            # Trigger the SaaS Flip Engine first
            api.post("/saas_flip_engine/attempt_sale", json={"saas_id": saas['id']})

        elif health_score > 0.6 and metrics['profit_margin'] > 0:
            decision = "MAINTAIN"
            print(f"DECISION for {saas['name']}: MAINTAIN (Stable)")

        # 4. Update the SaaS product's status
        api.patch(f"/saas_portfolio/{saas['id']}", json={
            "status": decision,
            "health_score": health_score
        })
```

## 3. API Interactions (Contracts)

- **`GET /idea_validator/top_ideas`**: Returns a list of validated idea objects.
- **`GET /financial_allocator/status`**: Returns `{discretionary_capital: float}`.
- **`GET /orchestrator/dev_capacity`**: Returns `{available_units: int}`.
- **`POST /orchestrator/dispatch_job`**: Dispatches a job (e.g., `INCUBATE_MVP`) to the agent workforce.
- **`GET /saas_portfolio/all`**: Returns a list of all SaaS product objects.
- **`GET /saas_portfolio/{id}/metrics`**: Returns a performance summary for a given SaaS.
- **`PATCH /saas_portfolio/{id}`**: Updates a SaaS product's status in the database.
- **`POST /campaign_manager/update_budget`**: Increases or decreases the marketing budget for a SaaS.
- **`POST /saas_flip_engine/attempt_sale`**: Initiates the process of selling a SaaS asset.
