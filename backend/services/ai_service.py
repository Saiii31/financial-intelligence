from sqlalchemy.orm import Session
from services.database_service import (
    get_dashboard_metrics,
    get_cashflow,
    get_expenses_by_category,
    get_liabilities,
    get_trends,
    get_health_score,
    get_anomalies,
    get_recommendations
)


def process_ai_question(question: str, db: Session):
    """
    Placeholder service for AI/LLM integration.
    This service provides financial data access for Person 4's AI agent.
    Person 4 will replace this with actual LLM integration.
    """
    
    financial_data = {
        "dashboard": get_dashboard_metrics(db),
        "cashflow": get_cashflow(db),
        "expenses": get_expenses_by_category(db),
        "liabilities": get_liabilities(db),
        "trends": get_trends(db),
        "health_score": get_health_score(db),
        "anomalies": get_anomalies(db),
        "recommendations": get_recommendations(db)
    }
    
    # Placeholder response - Person 4 will integrate actual LLM here
    answer = "AI integration pending. Person 4 will implement LLM-based responses."
    sources = ["dashboard", "cashflow", "expenses", "liabilities", "trends"]
    
    return {
        "answer": answer,
        "sources": sources
    }
