from pydantic import BaseModel
from datetime import date


class LiabilityItem(BaseModel):
    type: str
    outstanding: float
    interest_rate: float
    emi: float
    due_date: date


class LiabilityResponse(BaseModel):
    liabilities: list[LiabilityItem]
