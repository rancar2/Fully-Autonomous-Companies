# CampaignManagerAgent Logic Specification

## 1. Objective

To define the core logic for the `CampaignManagerAgent`, which autonomously designs, budgets, executes, and optimizes multi-channel marketing campaigns to drive customer acquisition.

## 2. Primary Functions & Logic

### 2.1. `design_and_budget_campaign()`

Triggered when a SaaS product enters the 'GROW' stage.

**Pseudocode:**

```python
def design_and_budget_campaign(saas_id):
    # 1. Get Product & Audience Information
    saas_product = api.get(f"/saas_portfolio/{saas_id}")
    customer_personas = api.get(f"/customer_growth/{saas_id}/personas")

    # 2. Request Initial Budget
    # The request is based on the product's potential and historical data
    budget_request = {
        "saas_id": saas_id,
        "requested_amount": calculate_initial_budget(saas_product),
        "purpose": f"Initial customer acquisition campaign for {saas_product['name']}"
    }
    allocated_budget = api.post("/financial_allocator/request_budget", json=budget_request)

    if allocated_budget['approved_amount'] == 0:
        print("HOLD: Budget request denied.")
        return

    # 3. Design Multi-Channel Campaign Strategy
    # Allocate budget across channels based on persona habitats
    campaign_plan = []
    for persona in customer_personas:
        for channel in persona['preferred_channels']:
            plan = {
                "channel": channel, # e.g., 'google_ads', 'reddit_ads', 'seo_content'
                "persona_id": persona['id'],
                "budget_allocation": allocated_budget['approved_amount'] * get_channel_weight(channel)
            }
            campaign_plan.append(plan)

    # 4. Dispatch Content Generation Jobs
    api.post("/orchestrator/dispatch_job", json={
        "job_type": "GENERATE_MARKETING_ASSETS",
        "saas_id": saas_id,
        "campaign_plan": campaign_plan
    })

    print(f"Campaign for {saas_product['name']} designed and budgeted. Awaiting content assets.")
```

### 2.2. `optimize_live_campaigns()`

This function runs on a continuous, daily loop for all active campaigns.

**Pseudocode:**

```python
def optimize_live_campaigns():
    active_campaigns = api.get("/campaign_manager/active_campaigns")

    for campaign in active_campaigns:
        # 1. Get performance data for the last 7 days
        performance = api.get(f"/marketing_performance/{campaign['id']}/summary?period=7d")

        # 2. Analyze Channel Performance (CAC and LTV)
        # The goal is to shift budget to channels with the lowest CAC and highest LTV
        channel_performance = []
        for channel_data in performance['channels']:
            cac = channel_data['spend'] / channel_data['conversions']
            ltv = channel_data['average_ltv']
            roi = ltv / cac
            channel_performance.append({"channel": channel_data['name'], "roi": roi})

        # 3. Re-allocate Budget
        # Identify the best and worst performing channels
        best_channel = max(channel_performance, key=lambda x: x['roi'])
        worst_channel = min(channel_performance, key=lambda x: x['roi'])

        if best_channel['roi'] > worst_channel['roi'] * 1.2: # Only shift if significant
            # Shift 10% of the budget from the worst to the best channel
            shift_amount = campaign['budget'] * 0.1
            print(f"OPTIMIZATION: Shifting ${shift_amount} from {worst_channel['channel']} to {best_channel['channel']}.")
            api.post("/campaign_manager/reallocate_budget", json={
                "campaign_id": campaign['id'],
                "from_channel": worst_channel['channel'],
                "to_channel": best_channel['channel'],
                "amount": shift_amount
            })

        # 4. Trigger Funnel Optimization
        # Alert the FunnelOptimizerAgent to focus on the top-performing channel
        api.post("/orchestrator/dispatch_job", json={
            "job_type": "OPTIMIZE_FUNNEL",
            "saas_id": campaign['saas_id'],
            "channel": best_channel['channel']
        })
```

## 3. API Interactions (Contracts)

- **`GET /saas_portfolio/{id}`**: Retrieves core product information.
- **`GET /customer_growth/{id}/personas`**: Returns a list of customer persona documents.
- **`POST /financial_allocator/request_budget`**: Submits a budget request to the AI-CFO.
- **`POST /orchestrator/dispatch_job`**: Dispatches jobs to other agents (e.g., `ContentCreatorAgent`).
- **`GET /campaign_manager/active_campaigns`**: Returns a list of all currently running campaigns.
- **`GET /marketing_performance/{id}/summary`**: Returns detailed performance metrics for a campaign.
- **`POST /campaign_manager/reallocate_budget`**: Executes a budget shift between marketing channels.
