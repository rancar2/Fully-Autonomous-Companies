# shared/api_client.py

import json

class APIClient:
    """A mock API client for inter-agent and external service communication."""

    def get(self, endpoint, params=None):
        print(f"[API] GET {endpoint} with params: {params}")
        # In a real implementation, this would make an HTTP request.
        # Here, we simulate responses based on the endpoint.
        if endpoint == "/idea_validator/top_ideas":
            return [{"id": 1, "name": "Podcast Show Notes Generator", "viability_score": 0.85}]
        if "/saas_portfolio/" in endpoint and "/metrics" in endpoint:
            return {"mrr_growth": 0.15, "user_satisfaction": 0.9, "churn_rate": 0.05, "profit_margin": 0.6}
        if endpoint == "/financial_analyst/monthly_summary":
            return {"net_profit_usd": 50000.0}
        # Add more mock responses as needed
        return {}

    def post(self, endpoint, json=None):
        print(f"[API] POST {endpoint} with json: {json}")
        # In a real implementation, this would make an HTTP request.
        if endpoint == "/orchestrator/dispatch_job":
            print(f"    -> Job dispatched: {json.get('job_type')} for SAAS ID {json.get('saas_id')}")
            return {"status": "success", "job_id": "job_123"}
        if endpoint == "/metamind/check_constitutionality":
            # Simulate that all hypotheses are safe for now
            return {"is_safe": True}
        return {"status": "success"}

    def patch(self, endpoint, json=None):
        print(f"[API] PATCH {endpoint} with json: {json}")
        return {"status": "success"}

# Global API client instance
api = APIClient()
