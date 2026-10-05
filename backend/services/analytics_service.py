from sqlalchemy.orm import Session
from models import FinancialMetric, MonthlyTrend, Recommendation


def save_financial_metrics(db: Session, metrics: dict):
    """
    Save financial metrics from Person 1's analytics.
    This will be used when integrating Person 1's verified results.
    """
    metric = FinancialMetric(
        income=metrics.get("income"),
        expenses=metrics.get("expenses"),
        savings=metrics.get("savings"),
        savings_rate=metrics.get("savings_rate"),
        total_assets=metrics.get("assets"),
        total_liabilities=metrics.get("liabilities"),
        net_worth=metrics.get("net_worth"),
        monthly_emi=metrics.get("monthly_emi"),
        debt_to_income=metrics.get("debt_to_income"),
        health_score=metrics.get("health_score")
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric


def save_monthly_trends(db: Session, trends: list):
    """
    Save monthly trends from Person 1's analytics.
    """
    for trend in trends:
        monthly_trend = MonthlyTrend(
            month=trend.get("month"),
            income=trend.get("income"),
            expenses=trend.get("expenses"),
            savings=trend.get("savings")
        )
        db.add(monthly_trend)
    db.commit()


def save_recommendations(db: Session, recommendations: list):
    """
    Save recommendations from Person 1's analytics.
    """
    for rec in recommendations:
        recommendation = Recommendation(
            recommendation=rec.get("recommendation"),
            priority=rec.get("priority"),
            category=rec.get("category")
        )
        db.add(recommendation)
    db.commit()
