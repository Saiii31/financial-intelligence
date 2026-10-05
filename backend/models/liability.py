from sqlalchemy import Column, Integer, String, DECIMAL, Date, TIMESTAMP
from database import Base


class Liability(Base):
    __tablename__ = "liabilities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    liability_id = Column(String(100), unique=True, nullable=False)
    type = Column(String(100), nullable=False)
    outstanding = Column(DECIMAL(15, 2), nullable=False)
    interest_rate = Column(DECIMAL(5, 2), nullable=False)
    emi = Column(DECIMAL(15, 2), nullable=False)
    due_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
