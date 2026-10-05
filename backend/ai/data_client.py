"""
The ONLY place the AI layer touches data. It calls Person 2's REST API
(the agreed JSON contract). The LLM never sees raw CSV/DB - only these results.
"""
import requests
from ai import config

MOCK = {
    "/api/dashboard": {"income": 223000, "expenses": 142000, "savings": 81000,
                       "savings_rate": 36.3, "net_worth": -2478000, "health_score": 74},
    "/api/cashflow": [
        {"month": "August", "income": 210000, "expenses": 120000, "savings": 90000},
        {"month": "September", "income": 223000, "expenses": 142000, "savings": 81000}],
    "/api/expenses": [
        {"category": "Housing", "amount": 80000, "percentage": 56.3},
        {"category": "Food", "amount": 45000, "percentage": 31.7},
        {"category": "Travel", "amount": 17000, "percentage": 12.0}],
    "/api/liabilities": [
        {"type": "Home Loan", "outstanding": 2850000, "interest_rate": 8.35, "emi": 28500},
        {"type": "Car Loan", "outstanding": 420000, "interest_rate": 9.1, "emi": 11200},
        {"type": "Credit Card", "outstanding": 68000, "interest_rate": 32, "emi": 7000}],
    "/api/trends": {"income_change": 12.5, "expense_change": 18.2, "savings_change": -8.3,
                    "top_spending_increase": {"category": "Travel", "change": 41}},
    "/api/recommendations": [
        {"priority": "HIGH", "category": "Debt", "recommendation": "Prioritize high-interest credit-card debt."},
        {"priority": "MEDIUM", "category": "Spending", "recommendation": "Review the increase in travel spending."}],
    "/api/transactions": [
        {"date": "2026-09-05", "category": "Food", "description": "Restaurant", "amount": 1200, "type": "expense"}],
}


def fetch(path: str):
    """Return JSON for an endpoint, or None if unavailable (caller must handle None)."""
    if config.USE_MOCK:
        return MOCK.get(path)
    try:
        r = requests.get(f"{config.API_BASE_URL}{path}", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[data_client] {path} failed: {e}")
        return None
