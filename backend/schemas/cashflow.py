from pydantic import BaseModel


class CashflowItem(BaseModel):
    month: str
    income: float
    expenses: float
    savings: float


class CashflowResponse(BaseModel):
    cashflow: list[CashflowItem]
