from sqlalchemy import Column, Integer, String, DECIMAL, Date, TIMESTAMP
from database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(String(100), unique=True, nullable=False)
    type = Column(String(100), nullable=False)
    value = Column(DECIMAL(15, 2), nullable=False)
    as_of_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
