from sqlalchemy import Column, Integer, DECIMAL, TIMESTAMP
from database import Base


class FinancialMetric(Base):
    __tablename__ = "financial_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    income = Column(DECIMAL(15, 2), nullable=False)
    expenses = Column(DECIMAL(15, 2), nullable=False)
    savings = Column(DECIMAL(15, 2), nullable=False)
    savings_rate = Column(DECIMAL(5, 2), nullable=False)
    total_assets = Column(DECIMAL(15, 2), nullable=False)
    total_liabilities = Column(DECIMAL(15, 2), nullable=False)
    net_worth = Column(DECIMAL(15, 2), nullable=False)
    monthly_emi = Column(DECIMAL(15, 2), nullable=False)
    debt_to_income = Column(DECIMAL(5, 2), nullable=False)
    health_score = Column(DECIMAL(5, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
