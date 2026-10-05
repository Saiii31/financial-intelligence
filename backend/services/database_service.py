from sqlalchemy.orm import Session
from models import (
    Transaction,
    Asset,
    Liability,
    FinancialMetric,
    MonthlyTrend,
    Recommendation
)


def get_dashboard_metrics(db: Session):
    metric = db.query(FinancialMetric).order_by(FinancialMetric.created_at.desc()).first()
    if metric:
        return {
            "income": float(metric.income),
            "expenses": float(metric.expenses),
            "savings": float(metric.savings),
            "savings_rate": float(metric.savings_rate),
            "assets": float(metric.total_assets),
            "liabilities": float(metric.total_liabilities),
            "net_worth": float(metric.net_worth),
            "debt_to_income": float(metric.debt_to_income),
            "health_score": float(metric.health_score)
        }
    return None


def get_cashflow(db: Session):
    trends = db.query(MonthlyTrend).order_by(MonthlyTrend.month).all()
    if not trends:
        return [
            {"month": "January", "income": 100000.0, "expenses": 70000.0, "savings": 30000.0},
            {"month": "February", "income": 110000.0, "expenses": 72000.0, "savings": 38000.0}
        ]
    return [
        {
            "month": trend.month,
            "income": float(trend.income),
            "expenses": float(trend.expenses),
            "savings": float(trend.savings)
        }
        for trend in trends
    ]


def get_expenses_by_category(db: Session):
    from sqlalchemy import func, text
    try:
        expenses = db.query(
            Transaction.category,
            func.sum(Transaction.amount).label('total')
        ).filter(Transaction.type == 'expense').group_by(Transaction.category).all()
        
        if not expenses:
            return [
                {"category": "Food", "amount": 45000.0, "percentage": 31.7},
                {"category": "Housing", "amount": 80000.0, "percentage": 56.3},
                {"category": "Transport", "amount": 17000.0, "percentage": 12.0}
            ]
        
        total_expenses = sum(float(exp[1]) for exp in expenses) if expenses else 0
        
        return [
            {
                "category": exp[0],
                "amount": float(exp[1]),
                "percentage": round(float(exp[1]) / total_expenses * 100, 1) if total_expenses > 0 else 0
            }
            for exp in expenses
        ]
    except Exception as e:
        print(f"Error in get_expenses_by_category: {e}")
        import traceback
        traceback.print_exc()
        return [
            {"category": "Food", "amount": 45000.0, "percentage": 31.7},
            {"category": "Housing", "amount": 80000.0, "percentage": 56.3},
            {"category": "Transport", "amount": 17000.0, "percentage": 12.0}
        ]


def get_liabilities(db: Session):
    liabilities = db.query(Liability).all()
    if not liabilities:
        from datetime import date
        return [
            {
                "type": "Credit Card",
                "outstanding": 100000.0,
                "interest_rate": 32.0,
                "emi": 10000.0,
                "due_date": date(2026, 10, 15)
            },
            {
                "type": "Personal Loan",
                "outstanding": 500000.0,
                "interest_rate": 12.0,
                "emi": 15000.0,
                "due_date": date(2026, 11, 1)
            }
        ]
    return [
        {
            "type": liability.type,
            "outstanding": float(liability.outstanding),
            "interest_rate": float(liability.interest_rate),
            "emi": float(liability.emi),
            "due_date": liability.due_date
        }
        for liability in liabilities
    ]


def get_trends(db: Session):
    trends = db.query(MonthlyTrend).order_by(MonthlyTrend.month).all()
    if len(trends) < 2:
        return {
            "income_change": 12.5,
            "expense_change": 18.2,
            "savings_change": -8.3,
            "top_spending_increase": {"category": "Travel", "change": 41.0}
        }
    
    # Find the last two months with actual income (not zero)
    valid_trends = [t for t in trends if float(t.income) > 0]
    if len(valid_trends) < 2:
        return {
            "income_change": 0.0,
            "expense_change": 0.0,
            "savings_change": 0.0,
            "top_spending_increase": {"category": "N/A", "change": 0}
        }
    
    latest = valid_trends[-1]
    previous = valid_trends[-2]
    
    income_change = round((float(latest.income) - float(previous.income)) / float(previous.income) * 100, 1) if previous.income > 0 else 0
    expense_change = round((float(latest.expenses) - float(previous.expenses)) / float(previous.expenses) * 100, 1) if previous.expenses > 0 else 0
    savings_change = round((float(latest.savings) - float(previous.savings)) / float(previous.savings) * 100, 1) if previous.savings > 0 else 0
    
    return {
        "income_change": income_change,
        "expense_change": expense_change,
        "savings_change": savings_change,
        "top_spending_increase": {"category": "N/A", "change": 0}
    }


def get_recommendations(db: Session):
    recommendations = db.query(Recommendation).order_by(Recommendation.created_at.desc()).all()
    if not recommendations:
        return [
            {
                "priority": "HIGH",
                "category": "Debt",
                "recommendation": "Prioritize high-interest credit-card debt."
            },
            {
                "priority": "MEDIUM",
                "category": "Spending",
                "recommendation": "Review the recent increase in travel spending."
            }
        ]
    return [
        {
            "priority": rec.priority,
            "category": rec.category,
            "recommendation": rec.recommendation
        }
        for rec in recommendations
    ]


def get_transactions(db: Session, category: str = None, type: str = None, start_date = None, end_date = None):
    query = db.query(Transaction)
    
    if category:
        query = query.filter(Transaction.category == category)
    if type:
        query = query.filter(Transaction.type == type)
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    transactions = query.order_by(Transaction.date.desc()).limit(100).all()
    
    if not transactions:
        from datetime import date
        return [
            {
                "txn_id": "TXN001",
                "date": date(2026, 10, 1),
                "category": "Food",
                "description": "Grocery shopping",
                "amount": 5000.0,
                "type": "expense",
                "is_duplicate": False,
                "is_anomaly": False
            },
            {
                "txn_id": "TXN002",
                "date": date(2026, 10, 2),
                "category": "Salary",
                "description": "Monthly salary",
                "amount": 100000.0,
                "type": "income",
                "is_duplicate": False,
                "is_anomaly": False
            }
        ]
    
    return [
        {
            "txn_id": txn.txn_id,
            "date": txn.date,
            "category": txn.category,
            "description": txn.description,
            "amount": float(txn.amount),
            "type": txn.type,
            "is_duplicate": txn.is_duplicate,
            "is_anomaly": txn.is_anomaly
        }
        for txn in transactions
    ]


def get_health_score(db: Session):
    metric = db.query(FinancialMetric).order_by(FinancialMetric.created_at.desc()).first()
    if metric:
        return float(metric.health_score)
    return None


def get_anomalies(db: Session):
    anomalies = db.query(Transaction).filter(Transaction.is_anomaly == True).all()
    return [
        {
            "txn_id": txn.txn_id,
            "date": txn.date,
            "category": txn.category,
            "description": txn.description,
            "amount": float(txn.amount)
        }
        for txn in anomalies
    ]
