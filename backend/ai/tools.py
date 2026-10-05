"""
Financial tools. Each returns a JSON string of VERIFIED data from Person 2's API.
Exact numbers come from here - never from the LLM.
"""
import json
from langchain_core.tools import tool
from ai.data_client import fetch


def _j(obj):
    return json.dumps(obj, ensure_ascii=False) if obj is not None else json.dumps({"error": "data unavailable"})


@tool
def get_dashboard_metrics() -> str:
    """Current income, expenses, savings, savings rate, net worth and health score."""
    return _j(fetch("/api/dashboard"))


@tool
def get_cashflow() -> str:
    """Monthly income, expenses and savings for every month."""
    return _j(fetch("/api/cashflow"))


@tool
def get_monthly_expenses(month: str = "") -> str:
    """Total expenses for a month (e.g. 'September'). Empty month = most recent month."""
    data = fetch("/api/cashflow")
    if not data:
        return _j(None)
    if month:
        for row in data:
            if month.lower() in str(row["month"]).lower():
                return _j({"month": row["month"], "expenses": row["expenses"]})
        return _j({"error": f"no data for month '{month}'"})
    last = data[-1]
    return _j({"month": last["month"], "expenses": last["expenses"], "note": "most recent month"})


@tool
def get_category_expenses(category: str = "") -> str:
    """Spending by category (amount and % of total). Optional category filter."""
    data = fetch("/api/expenses")
    if data and category:
        data = [d for d in data if category.lower() in d["category"].lower()]
    return _j(data)


@tool
def get_liabilities() -> str:
    """All debts: type, outstanding, interest rate, EMI."""
    data = fetch("/api/liabilities")
    if data:  # helper facts computed in Python, not by the LLM
        total = sum(d["outstanding"] for d in data)
        emi = sum(d["emi"] for d in data)
        highest = max(data, key=lambda d: d["interest_rate"])
        return _j({"liabilities": data, "total_outstanding": total,
                   "total_monthly_emi": emi, "highest_interest": highest})
    return _j(None)


@tool
def get_trends() -> str:
    """Month-over-month % change in income, expenses, savings and top spending increase."""
    return _j(fetch("/api/trends"))


@tool
def get_recommendations() -> str:
    """Existing rule-based recommendations with priority."""
    return _j(fetch("/api/recommendations"))


@tool
def get_transactions(category: str = "", limit: int = 10) -> str:
    """Recent transactions, optionally filtered by category."""
    data = fetch("/api/transactions")
    if not data:
        return _j({"error": "transaction data unavailable"})
    if category:
        data = [t for t in data if category.lower() in t["category"].lower()]
    data = sorted(data, key=lambda t: t["date"], reverse=True)[:limit]
    return _j(data)


@tool
def semantic_financial_search(query: str) -> str:
    """Semantic (FAISS) search over financial documents for contextual questions."""
    from ai.retriever import search
    return _j(search(query))


TOOLS = {t.name: t for t in [
    get_dashboard_metrics, get_cashflow, get_monthly_expenses, get_category_expenses,
    get_liabilities, get_trends, get_recommendations, get_transactions,
    semantic_financial_search]}
