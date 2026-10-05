from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP
from database import Base


class MonthlyTrend(Base):
    __tablename__ = "monthly_trends"

    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(String(20), nullable=False)
    income = Column(DECIMAL(15, 2), nullable=False)
    expenses = Column(DECIMAL(15, 2), nullable=False)
    savings = Column(DECIMAL(15, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
