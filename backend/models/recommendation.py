from sqlalchemy import Column, Integer, String, TIMESTAMP
from database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recommendation = Column(String(500), nullable=False)
    priority = Column(String(20), nullable=False)
    category = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
