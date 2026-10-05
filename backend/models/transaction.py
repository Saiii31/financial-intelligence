from sqlalchemy import Column, Integer, String, Date, Text, DECIMAL, Boolean, TIMESTAMP
from database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    txn_id = Column(String(100), unique=True, nullable=False)
    date = Column(Date, nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text)
    amount = Column(DECIMAL(15, 2), nullable=False)
    type = Column(String(20), nullable=False)
    is_duplicate = Column(Boolean, default=False)
    is_anomaly = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
